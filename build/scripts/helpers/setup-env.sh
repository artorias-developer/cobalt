#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Checking .env files..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV="prod"
DOMAIN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prod) ENV="prod" ;;
    --dev)  ENV="dev"  ;;
    --local)
      if [[ -n "${2:-}" && "${2:-}" != --* ]]; then
        DOMAIN="$2"
        shift
      else
        DOMAIN="127.0.0.1"
      fi
      ;;
    --vps)
      shift
      if [[ -z "$1" ]]; then
        echo "Usage: $0 --vps <ip>"
        exit 1
      fi
      DOMAIN="$1"
      ;;
    *)
      echo "Usage: $0 [--prod|--dev] [--local [domain]|--vps <ip>]"
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$DOMAIN" ]]; then
  echo "Error: specify --local [domain] or --vps <ip>"
  exit 1
fi

TARGET="$SCRIPT_DIR/../../$ENV"

GLOBAL_SALT=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -hex 24)
REDIS_PASSWORD=$(openssl rand -hex 24)

generate() {
  local dest="$1"
  local src="$2"
  local args="${@:3}"
  local name
  name=$(basename "$dest")

  if [[ -f "$dest" ]]; then
    echo "  Skipping $name (already exists)."
    return
  fi

  sed $args "$src" > "$dest"
  echo "  The $name file has been successfully generated."
}

copy() {
  local dest="$1"
  local src="$2"
  local name
  name=$(basename "$dest")

  if [[ -f "$dest" ]]; then
    echo "  Skipping $name (already exists)."
    return
  fi

  cp "$src" "$dest"
  echo "  The $name file has been successfully generated."
}

generate "$TARGET/backend/.env" "$TARGET/backend/.env.example" \
  -e "s/{{global_salt}}/$GLOBAL_SALT/" \
  -e "s/{{postgres_password}}/$POSTGRES_PASSWORD/" \
  -e "s/{{redis_password}}/$REDIS_PASSWORD/" \
  -e "s/{{domain}}/$DOMAIN/"

generate "$TARGET/postgres/.env" "$TARGET/postgres/.env.example" \
  -e "s/{{postgres_password}}/$POSTGRES_PASSWORD/"

generate "$TARGET/redis/.env" "$TARGET/redis/.env.example" \
  -e "s/{{redis_password}}/$REDIS_PASSWORD/"

copy "$TARGET/frontend/.env" "$TARGET/frontend/.env.example"
copy "$TARGET/nginx/.env"    "$TARGET/nginx/.env.example"
