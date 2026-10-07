#!/bin/bash

#
# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later
#

set -e
shopt -s nullglob dotglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

MOVED=0

move() {
  local src="$1"
  local dst="$2"

  [[ -e "$src" ]] || return 0

  if [[ -e "$dst" ]]; then
    echo "  Skipped (target exists): ${dst#"$ROOT"/}"
    return 0
  fi

  mkdir -p "$(dirname "$dst")"

  if ! mv "$src" "$dst"; then
    echo "Error: cannot move ${src#"$ROOT"/} (permission denied?)."
    echo "Try: sudo chown -R $USER:$USER \"$src\""
    exit 1
  fi

  echo "  Moved: ${src#"$ROOT"/} -> ${dst#"$ROOT"/}"
  MOVED=$((MOVED + 1))
}

echo "Checking project layout..."

for env in dev prod; do
  for service in backend postgres redis nginx frontend; do
    dst="$ROOT/generated/$env/build/$service/.env"

    move "$ROOT/build/$env/$service/.env" "$dst"

    if [[ "$env" == "prod" && -f "$dst" ]]; then
      chmod 600 "$dst"
    fi
  done

  old_ssl="$ROOT/build/$env/nginx/ssl"

  for crt in "$old_ssl"/*.crt; do
    name="$(basename "$crt" .crt)"
    key="$old_ssl/$name.key"
    out="$ROOT/generated/$env/build/nginx/ssl/self-signed/$name"

    if [[ ! -f "$key" ]]; then
      echo "  Skipped (no matching key): ${crt#"$ROOT"/}"
      continue
    fi

    move "$crt" "$out/fullchain.pem"
    move "$key" "$out/privkey.pem"
  done

  rmdir "$old_ssl" 2>/dev/null || true
done

old_generated="$ROOT/cobalt/backend/generated"
new_generated="$ROOT/generated/dev/backend"

if [[ -d "$old_generated" ]]; then
  for item in "$old_generated"/*; do
    move "$item" "$new_generated/$(basename "$item")"
  done

  rmdir "$old_generated" 2>/dev/null || true
fi

if [[ "$MOVED" -eq 0 ]]; then
  echo "  Layout is up to date."
else
  echo "  Layout migration finished: $MOVED item(s) moved."
fi