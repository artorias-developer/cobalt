#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

SERVER_CONFIG="$INSTALLATION_DIR/serverconfig.cfg"

function sync_files() {
    rsync -a \
        --exclude 'installer.sh' \
        "$INSTALLATION_DIR/." "$SERVER_ROOT/"
}

function setup_config() {
    if [ -f "$SERVER_CONFIG" ]; then
        sed -i "s|{SERVER_ROOT}|$SERVER_ROOT|g" "$SERVER_CONFIG"
    fi
}

function main() {
    setup_config
    sync_files
    echo "Install successful."
}

main