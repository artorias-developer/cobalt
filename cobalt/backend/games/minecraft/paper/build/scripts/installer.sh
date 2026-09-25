#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

function sync_files() {
    rsync -a \
        --exclude 'installer.sh' \
        "$INSTALLATION_DIR/." "$SERVER_ROOT/"
}

function main() {
    sync_files
    echo "Install successful."
}

main