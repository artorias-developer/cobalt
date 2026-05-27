#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Checking self-signed SSL certificates..."

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
        echo "Usage: $0 [--prod|--dev] [--local [domain]|--vps <ip>]"
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

SSL_DIR="$SCRIPT_DIR/../../$ENV/nginx/ssl"

mkdir -p "$SSL_DIR"
chmod 755 "$SSL_DIR"

if [[ -f "$SSL_DIR/server.crt" && -f "$SSL_DIR/server.key" ]]; then
  echo "  Skipping SSL certificates (already exist)."
  exit 0
fi

openssl req -x509 -nodes -newkey rsa:4096 \
  -keyout "$SSL_DIR/server.key" \
  -out "$SSL_DIR/server.crt" \
  -days 3650 \
  -subj "/CN=$DOMAIN" \
  -addext "subjectAltName=IP:$DOMAIN"

echo "  SSL certificates have been successfully generated."