#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_BIN="$SERVER_ROOT/bin/x64/factorio"
DATA_DIR="$SERVER_ROOT/data"
MODS_DIR="$SERVER_ROOT/mods"
SERVER_SETTINGS="$DATA_DIR/server-settings.json"
MAP_SETTINGS="$DATA_DIR/map-settings.json"
MAP_GEN_SETTINGS="$DATA_DIR/map-gen-settings.json"
SERVER_WHITELIST="$DATA_DIR/server-whitelist.json"
SERVER_BANLIST="$DATA_DIR/server-banlist.json"
SERVER_ADMINLIST="$DATA_DIR/server-adminlist.json"
MAP_FILE="map.zip"
MAP_SAVE="$SERVER_ROOT/saves/$MAP_FILE"

SERVER_PID=""
FIFO_HOLDER_PID=""

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# --start-server
# --server-settings
# --map-settings
# --server-banlist
# --server-adminlist
# --use-server-whitelist
# --server-whitelist
# --mod-directory
SERVER_ARGS=(
    --start-server "$MAP_SAVE"
    --mod-directory "$MODS_DIR"
)

function stop_server() {
    if [ -p "$SERVER_FIFO" ] && [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "/quit" > "$SERVER_FIFO" 2>/dev/null

        for i in {1..60}; do
            if ! kill -0 "$SERVER_PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done

        if kill -0 "$SERVER_PID" 2>/dev/null; then
            kill -9 "$SERVER_PID" 2>/dev/null
        fi
    fi

    if [ -n "$FIFO_HOLDER_PID" ]; then
        kill "$FIFO_HOLDER_PID" 2>/dev/null
    fi

    rm -f "$SERVER_FIFO"
    exit 0
}

function create_map() {
    if [ -f "$MAP_SAVE" ]; then
        return
    fi

    if [ "$HAS_RELATIVE_CREATE_PATH" = "true" ]; then
        CREATE_PATH="$MAP_FILE"
    else
        CREATE_PATH="$MAP_SAVE"
    fi

    CREATE_ARGS=(
        --create "$CREATE_PATH"
    )

    if [ -f "$MAP_GEN_SETTINGS" ]; then
        CREATE_ARGS+=(--map-gen-settings "$MAP_GEN_SETTINGS")
    fi

    if [ -f "$MAP_SETTINGS" ]; then
        CREATE_ARGS+=(--map-settings "$MAP_SETTINGS")
    fi

    "$SERVER_BIN" "${CREATE_ARGS[@]}" > >(filter_log)
}

function setup_fifo() {
    rm -f "$SERVER_FIFO"
    mkfifo "$SERVER_FIFO"
}

function start_fifo_holder() {
    sleep infinity > "$SERVER_FIFO" &
    FIFO_HOLDER_PID=$!
}

function configure_server_args() {
    if [ "$HAS_SERVER_SETTINGS_OPTION" = "true" ] && [ -f "$SERVER_SETTINGS" ]; then
        SERVER_ARGS+=(--server-settings "$SERVER_SETTINGS")
    fi

    if [ -f "$MAP_SETTINGS" ]; then
        SERVER_ARGS+=(--map-settings "$MAP_SETTINGS")
    fi

    if [ "$HAS_BANLIST_OPTION" = "true" ] && [ -f "$SERVER_BANLIST" ]; then
        SERVER_ARGS+=(--server-banlist "$SERVER_BANLIST")
    fi

    if [ "$HAS_ADMIN_LIST_OPTION" = "true" ] && [ -f "$SERVER_ADMINLIST" ]; then
        SERVER_ARGS+=(--server-adminlist "$SERVER_ADMINLIST")
    fi

    if [ "$HAS_WHITELIST_OPTION" = "true" ] && [ -f "$SERVER_WHITELIST" ]; then
        if [ "$HAS_USE_WHITELIST_OPTION" = "true" ]; then
            SERVER_ARGS+=(--use-server-whitelist --server-whitelist "$SERVER_WHITELIST")
        else
            SERVER_ARGS+=(--server-whitelist "$SERVER_WHITELIST")
        fi
    fi
}

function filter_log() {
    sed -u -E \
        -e 's/^\s*[0-9]+\.[0-9]+ //' \
        -e 's/^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2};? //' \
        -e 's/^(Info|Warning|Error) [A-Za-z0-9_]+\.cpp:[0-9]+: //'
}

function start_server() {
    "$SERVER_BIN" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" > >(filter_log) &
    SERVER_PID=$!
}

function main() {
    trap stop_server SIGINT SIGTERM

    create_map
    setup_fifo
    start_fifo_holder
    configure_server_args
    start_server

    wait $SERVER_PID
}

main