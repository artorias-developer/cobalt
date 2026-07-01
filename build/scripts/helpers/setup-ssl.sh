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
    --server)
      shift
      if [[ -z "$1" ]]; then
        echo "Usage: $0 [--prod|--dev] [--local [domain]|--server <ip>]"
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

SSL_DIR="$SCRIPT_DIR/../../$ENV/nginx/ssl"

mkdir -p "$SSL_DIR"
chmod 755 "$SSL_DIR"

SAFE_DOMAIN="${DOMAIN//:/_}"
CERT_FILE="$SSL_DIR/$SAFE_DOMAIN.crt"
KEY_FILE="$SSL_DIR/$SAFE_DOMAIN.key"
ACTION="generated"

if [[ -f "$CERT_FILE" && -f "$KEY_FILE" ]]; then
  ACTION="replaced"
fi

if [[ "$DOMAIN" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
  SAN="IP:$DOMAIN"
else
  SAN="DNS:$DOMAIN"
fi

openssl req -x509 -nodes -newkey rsa:4096 \
  -keyout "$KEY_FILE" \
  -out "$CERT_FILE" \
  -days 3650 \
  -subj "/CN=$DOMAIN" \
  -addext "subjectAltName=$SAN"

echo "  SSL certificates ($SAFE_DOMAIN.crt / $SAFE_DOMAIN.key) have been successfully $ACTION."