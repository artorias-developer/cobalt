#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e

SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER_DIRECTORY="$SCRIPT_DIRECTORY/installer"
MINIMUM_NODE_MAJOR_VERSION=18
NVM_VERSION="v0.40.8"
NODE_INSTALL_VERSION=24

if [[ ! -t 0 || ! -t 1 ]]; then
  echo "Error: the installer must be run in an interactive terminal."
  exit 1
fi

is_ubuntu() {
  [[ -r /etc/os-release ]] || return 1
  . /etc/os-release
  [[ "${ID:-}" == "ubuntu" || "${ID_LIKE:-}" == *ubuntu* ]]
}

case "$(uname -s)" in
  Darwin) ;;
  Linux)
    if ! is_ubuntu; then
      echo "Error: unsupported Linux distribution. Only Ubuntu and macOS are supported."
      exit 1
    fi
    ;;
  *)
    echo "Error: unsupported OS. Only Ubuntu and macOS are supported."
    exit 1
    ;;
esac

install_curl() {
  echo "Installing curl..."
  local sudo_cmd=""
  if [[ $EUID -ne 0 ]]; then
    sudo_cmd="sudo"
  fi
  $sudo_cmd apt-get update -qq
  $sudo_cmd env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq curl ca-certificates
}

load_nvm() {
  export NVM_DIR="${NVM_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/nvm}"
  [[ -s "$NVM_DIR/nvm.sh" ]] || export NVM_DIR="$HOME/.nvm"
  if [[ -s "$NVM_DIR/nvm.sh" ]]; then
    set +e
    \. "$NVM_DIR/nvm.sh"
    set -e
  fi
}

is_node_available() {
  command -v node &>/dev/null && command -v npm &>/dev/null || return 1
  local major_version
  major_version="$(node -p 'process.versions.node.split(".")[0]')"
  (( major_version >= MINIMUM_NODE_MAJOR_VERSION ))
}

load_nvm

if ! is_node_available; then
  if ! command -v curl &>/dev/null; then
    install_curl
  fi

  if ! command -v nvm &>/dev/null; then
    echo "Installing nvm $NVM_VERSION..."
    curl -o- "https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VERSION/install.sh" | bash
    load_nvm
  fi

  echo "Installing Node.js $NODE_INSTALL_VERSION..."
  set +e
  nvm install "$NODE_INSTALL_VERSION"
  nvm_status=$?
  set -e
  if (( nvm_status != 0 )); then
    echo "Error: failed to install Node.js via nvm."
    exit 1
  fi

  echo "Node: $(node -v), npm: $(npm -v)"
fi

if [[ ! -d "$INSTALLER_DIRECTORY/node_modules/@clack/prompts" ]]; then
  echo "Installing installer dependencies..."
  npm install --prefix "$INSTALLER_DIRECTORY" --no-audit --no-fund --loglevel=error
fi

export COBALT_INSTALL_DIR="$SCRIPT_DIRECTORY"
exec node "$INSTALLER_DIRECTORY/cli.mjs"