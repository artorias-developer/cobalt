#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
export DEBIAN_FRONTEND=noninteractive

SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER_DIRECTORY="$SCRIPT_DIRECTORY/installer"
MINIMUM_NODE_MAJOR_VERSION=18

if [[ ! -t 0 || ! -t 1 ]]; then
  echo "Error: the installer must be run in an interactive terminal."
  exit 1
fi

is_node_available() {
  command -v node &>/dev/null && command -v npm &>/dev/null || return 1
  local major_version
  major_version="$(node -p 'process.versions.node.split(".")[0]')"
  (( major_version >= MINIMUM_NODE_MAJOR_VERSION ))
}

if ! is_node_available; then
  echo "Installing Node.js..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq ca-certificates curl gnupg
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - >/dev/null
  sudo apt-get install -y -qq nodejs
fi

if [[ ! -d "$INSTALLER_DIRECTORY/node_modules/@clack/prompts" ]]; then
  echo "Installing installer dependencies..."
  npm install --prefix "$INSTALLER_DIRECTORY" --no-audit --no-fund --loglevel=error
fi

export COBALT_INSTALL_DIR="$SCRIPT_DIRECTORY"
exec node "$INSTALLER_DIRECTORY/cli.mjs"