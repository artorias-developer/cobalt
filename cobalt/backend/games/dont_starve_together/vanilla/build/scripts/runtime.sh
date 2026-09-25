#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

SERVER_BIN="$SERVER_ROOT/bin/dontstarve_dedicated_server_nullrenderer"

SERVER_PID=""
FIFO_HOLDER_PID=""

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# -persistent_storage_root
# -conf_dir
# -cluster
# -shard
SERVER_ARGS=(
    -persistent_storage_root "$SERVER_ROOT"
    -conf_dir DoNotStarveTogether
    -cluster cluster
    -shard Main
)

function stop_server() {
    if [ -p "$SERVER_FIFO" ] && [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "c_shutdown()" > "$SERVER_FIFO" 2>/dev/null

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

function filter_log() {
    sed -u -E 's/^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]: //'
}

function start_server() {
    cd "$SERVER_ROOT/bin"

    "$SERVER_BIN" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" > >(filter_log) &
    SERVER_PID=$!
}

function main() {
    trap stop_server SIGINT SIGTERM

    setup_fifo
    start_fifo_holder
    start_server

    wait $SERVER_PID
}

main