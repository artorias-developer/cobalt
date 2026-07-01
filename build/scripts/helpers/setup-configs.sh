#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Checking config files..."

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
    --server)
      shift
      if [[ -z "$1" ]]; then
        echo "Usage: $0 --server <ip>"
        exit 1
      fi
      DOMAIN="$1"
      ;;
    *)
      echo "Usage: $0 [--prod|--dev] [--local [domain]|--server <ip>]"
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$DOMAIN" ]]; then
  echo "Error: specify --local [domain] or --server <ip>"
  exit 1
fi

TARGET="$SCRIPT_DIR/../../$ENV"
ROOT="$SCRIPT_DIR/../../.."

GLOBAL_SALT=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -hex 24)
REDIS_PASSWORD=$(openssl rand -hex 24)

generate() {
  local dest="$1"
  local src="$2"
  local args="${@:3}"
  local name
  name=$(basename "$(dirname "$dest")")/$(basename "$dest")
  local action="generated"

  if [[ -f "$dest" ]]; then
    action="replaced"
  fi

  sed $args "$src" > "$dest"
  echo "  The $name file has been successfully $action."
}

copy() {
  local dest="$1"
  local src="$2"
  local name
  name=$(basename "$(dirname "$dest")")/$(basename "$dest")
  local action="generated"

  if [[ -f "$dest" ]]; then
    action="replaced"
  fi

  cp "$src" "$dest"
  echo "  The $name file has been successfully $action."
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

generate "$TARGET/nginx/.env" "$TARGET/nginx/.env.example" \
  -e "s/{{domain}}/$DOMAIN/"

copy "$TARGET/frontend/.env" "$TARGET/frontend/.env.example"

ALEMBIC_DEST="$ROOT/cobalt/backend/alembic.ini"
ALEMBIC_SRC="$ROOT/cobalt/backend/alembic.ini.example"
ALEMBIC_ACTION="generated"

if [[ -f "$ALEMBIC_DEST" ]]; then
  ALEMBIC_ACTION="replaced"
fi

cp "$ALEMBIC_SRC" "$ALEMBIC_DEST"
echo "  The alembic.ini file has been successfully $ALEMBIC_ACTION."