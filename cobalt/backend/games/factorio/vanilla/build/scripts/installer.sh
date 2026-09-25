#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

DATA_DIR="$INSTALLATION_DIR/data"
SERVER_DATA_DIR="$SERVER_ROOT/data"

function sync_files() {
    rsync -a \
        --exclude 'installer.sh' \
        "$INSTALLATION_DIR/." "$SERVER_ROOT/"
}

function remove_example_configs() {
    [ -f "$SERVER_DATA_DIR/map-gen-settings.example.json" ] && rm -f "$SERVER_DATA_DIR/map-gen-settings.example.json"
    [ -f "$SERVER_DATA_DIR/map-settings.example.json" ] && rm -f "$SERVER_DATA_DIR/map-settings.example.json"
    [ -f "$SERVER_DATA_DIR/server-settings.example.json" ] && rm -f "$SERVER_DATA_DIR/server-settings.example.json"
    [ -f "$SERVER_DATA_DIR/server-whitelist.example.json" ] && rm -f "$SERVER_DATA_DIR/server-whitelist.example.json"
    return 0
}

function remove_disabled_options() {
    if [ "$HAS_SERVER_SETTINGS_OPTION" != "true" ]; then rm -f "$DATA_DIR/server-settings.json"; fi
    if [ "$HAS_WHITELIST_OPTION" != "true" ]; then rm -f "$DATA_DIR/server-whitelist.json"; fi
    if [ "$HAS_BANLIST_OPTION" != "true" ]; then rm -f "$DATA_DIR/server-banlist.json"; fi
    if [ "$HAS_ADMIN_LIST_OPTION" != "true" ]; then rm -f "$DATA_DIR/server-adminlist.json"; fi
}

function main() {
    remove_disabled_options
    sync_files
    remove_example_configs
    echo "Install successful."
}

main