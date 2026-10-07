#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Checking config files..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV="prod"
DOMAIN=""
NO_ADMIN_BASE="false"

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
      if [[ -z "${1:-}" ]]; then
        echo "Usage: $0 --server <ip>"
        exit 1
      fi
      DOMAIN="$1"
      ;;
    --no-admin-base)
      NO_ADMIN_BASE="true"
      ;;
    *)
      echo "Usage: $0 [--prod|--dev] [--local [domain]|--server <ip>] [--no-admin-base]"
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$DOMAIN" ]]; then
  echo "Error: specify --local [domain] or --server <ip>"
  exit 1
fi

ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SRC_DIR="$ROOT/build/$ENV"
OUT_DIR="$ROOT/generated/$ENV/build"

PEPPER=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -hex 24)
REDIS_PASSWORD=$(openssl rand -hex 24)

if [[ "$NO_ADMIN_BASE" == "true" ]]; then
  APP_BASE_URL=""
else
  APP_BASE_URL=$(openssl rand -hex 16)
fi

generate() {
  local service="$1"
  local src="$SRC_DIR/$service/.env.example"
  local dest="$OUT_DIR/$service/.env"
  local action="generated"

  [[ -f "$dest" ]] && action="replaced"

  mkdir -p "$(dirname "$dest")"
  sed "${@:2}" "$src" > "$dest"

  if [[ "$ENV" == "prod" ]]; then
    chmod 600 "$dest"
  fi

  echo "  The $service/.env file has been successfully $action."
}

generate backend \
  -e "s/{{pepper}}/$PEPPER/" \
  -e "s/{{postgres_password}}/$POSTGRES_PASSWORD/" \
  -e "s/{{redis_password}}/$REDIS_PASSWORD/" \
  -e "s/{{domain}}/$DOMAIN/"

generate postgres \
  -e "s/{{postgres_password}}/$POSTGRES_PASSWORD/"

generate redis \
  -e "s/{{redis_password}}/$REDIS_PASSWORD/"

generate nginx \
  -e "s/{{domain}}/$DOMAIN/" \
  -e "s|{{base_url}}|$APP_BASE_URL|"

generate frontend \
  -e "s|{{domain}}|$DOMAIN|" \
  -e "s|{{base_url}}|$APP_BASE_URL|"

ALEMBIC_DEST="$ROOT/cobalt/backend/alembic.ini"
ALEMBIC_SRC="$ROOT/cobalt/backend/alembic.ini.example"
ALEMBIC_ACTION="generated"

if [[ -f "$ALEMBIC_DEST" ]]; then
  ALEMBIC_ACTION="replaced"
fi

cp "$ALEMBIC_SRC" "$ALEMBIC_DEST"
echo "  The alembic.ini file has been successfully $ALEMBIC_ACTION."

if [[ -n "${SUMMARY_FILE:-}" ]]; then
  {
    echo "DOMAIN=$DOMAIN"
    echo "APP_BASE_URL=$APP_BASE_URL"
  } > "$SUMMARY_FILE"
fi