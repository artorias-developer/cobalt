#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_BIN="$SERVER_ROOT/LaunchUtils/ScriptCaller.sh"
CONFIG_RUNTIME="$SERVER_ROOT/serverconfig.cfg"

SERVER_PID=""
FIFO_HOLDER_PID=""

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# -server
# -nosteam
# -tmlsavedirectory
# -config
SERVER_ARGS=(
    -server
    -nosteam
    -tmlsavedirectory "$SERVER_ROOT/data"
)

function stop_server() {
    if [ -p "$SERVER_FIFO" ] && [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "exit" > "$SERVER_FIFO" 2>/dev/null

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

function setup_fifo() {
    rm -f "$SERVER_FIFO"
    mkfifo "$SERVER_FIFO"
}

function start_fifo_holder() {
    sleep infinity > "$SERVER_FIFO" &
    FIFO_HOLDER_PID=$!
}

function configure_server_args() {
    if [ -f "$CONFIG_RUNTIME" ]; then
        SERVER_ARGS+=(-config "$CONFIG_RUNTIME")
    fi
}

function start_server() {
    "$SERVER_BIN" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
    SERVER_PID=$!
}

function main() {
    trap stop_server SIGINT SIGTERM

    setup_fifo
    start_fifo_holder
    configure_server_args
    start_server

    wait $SERVER_PID
}

main