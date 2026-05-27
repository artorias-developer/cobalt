#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Checking the alembic.ini file..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/../../.."
DEST="$ROOT/cobalt/backend/alembic.ini"
SRC="$ROOT/cobalt/backend/alembic.ini.example"

if [[ -f "$DEST" ]]; then
  echo "  Skipping alembic.ini (already exists)."
  exit 0
fi

cp "$SRC" "$DEST"

echo "  The alembic.ini file has been successfully generated."