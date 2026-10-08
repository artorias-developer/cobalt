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

TARGET_ENV="prod"

usage() {
  echo "Usage: $0 [--dev | --prod]"
  echo "  The flag sets which environment the old cobalt/backend/generated belongs to."
  echo "  Default: --prod"
}

for arg in "$@"; do
  case "$arg" in
    --dev)  TARGET_ENV="dev" ;;
    --prod) TARGET_ENV="prod" ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

MOVED=0
SKIPPED=0

move() {
  local src="$1"
  local dst="$2"

  [[ -e "$src" || -L "$src" ]] || return 0

  if [[ -e "$dst" || -L "$dst" ]]; then
    if [[ -f "$src" && -f "$dst" ]] && cmp -s "$src" "$dst"; then
      echo "  Skipped (target exists, identical): ${dst#"$ROOT"/}"
    else
      echo "  Skipped (target exists, DIFFERS):   ${dst#"$ROOT"/}"
    fi
    SKIPPED=$((SKIPPED + 1))
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

merge_move() {
  local src="$1"
  local dst="$2"

  [[ -e "$src" || -L "$src" ]] || return 0

  if [[ -d "$src" && ! -L "$src" && -d "$dst" && ! -L "$dst" ]]; then
    local item
    for item in "$src"/*; do
      merge_move "$item" "$dst/$(basename "$item")"
    done
    rmdir "$src" 2>/dev/null || true
    return 0
  fi

  move "$src" "$dst"
}

echo "Checking project layout..."
echo "  ROOT:       $ROOT"
echo "  TARGET_ENV: $TARGET_ENV"

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
new_generated="$ROOT/generated/$TARGET_ENV/backend"

echo "  Old generated: ${old_generated#"$ROOT"/}"
echo "  New generated: ${new_generated#"$ROOT"/}"

if [[ -d "$old_generated" ]]; then
  for item in "$old_generated"/*; do
    echo "  Found: ${item#"$ROOT"/}"
    merge_move "$item" "$new_generated/$(basename "$item")"
  done

  rmdir "$old_generated" 2>/dev/null || true
else
  echo "  Old generated folder NOT FOUND at that path."
fi

if [[ "$MOVED" -eq 0 && "$SKIPPED" -eq 0 ]]; then
  echo "  Nothing to move."
else
  echo "  Done: $MOVED moved, $SKIPPED skipped."
fi