#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."
ENV="prod"
DOMAIN_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prod) ENV="prod" ;;
    --dev)  ENV="dev"  ;;
    --local)
      if [[ -n "${2:-}" && "${2:-}" != --* ]]; then
        DOMAIN_ARG="--local $2"
        shift
      else
        DOMAIN_ARG="--local"
      fi
      ;;
    --vps)
      shift
      if [[ -z "$1" ]]; then
        echo "Usage: $0 [--prod|--dev] [--local [domain]|--vps <ip>]"
        exit 1
      fi
      DOMAIN_ARG="--vps $1"
      ;;
    *)
      echo "Usage: $0 [--prod|--dev] [--local [domain]|--vps <ip>]"
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$DOMAIN_ARG" ]]; then
  echo "Error: specify --local [domain] or --vps <ip>"
  exit 1
fi

bash "$SCRIPT_DIR/helpers/setup-docker.sh"
bash "$SCRIPT_DIR/helpers/setup-ssl.sh" "--$ENV" $DOMAIN_ARG
bash "$SCRIPT_DIR/helpers/setup-env.sh" "--$ENV" $DOMAIN_ARG

echo "Starting containers..."
docker compose -f "$ROOT/$ENV/docker-compose.yaml" up -d --build

echo "Cobalt has been successfully launched."