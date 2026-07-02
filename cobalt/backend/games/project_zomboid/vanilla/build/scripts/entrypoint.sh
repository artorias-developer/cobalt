#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_ROOT="${SERVER_ROOT:-/opt/cobalt_server}"
SERVER_FIFO="${SERVER_FIFO:-/tmp/cobalt_server_fifo}"

SERVER_NAME="serverconfig"
SERVER_BIN="$SERVER_ROOT/start-server.sh"
CACHE_DIR="$SERVER_ROOT/Zomboid"
SERVER_DIR="$SERVER_ROOT/Zomboid/Server"
SERVER_INI="$SERVER_DIR/${SERVER_NAME}.ini"

SERVER_PID=""

function stop_server() {
    if [ -p "$SERVER_FIFO" ] && [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "quit" > "$SERVER_FIFO" 2>/dev/null

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

trap stop_server SIGINT SIGTERM

if [ -f "$SERVER_INI" ]; then
    sed -i "s|{SERVER_DEFAULT_PORT}|$SERVER_DEFAULT_PORT|g" "$SERVER_INI"
    sed -i "s|{SERVER_UDP_PORT}|$SERVER_UDP_PORT|g" "$SERVER_INI"
fi

rm -f "$SERVER_FIFO"
mkfifo "$SERVER_FIFO"

sleep infinity > "$SERVER_FIFO" &
FIFO_HOLDER_PID=$!

cd "$SERVER_ROOT"

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# -servername
# -cachedir
SERVER_ARGS=(
    -servername "$SERVER_NAME"
    -cachedir="$CACHE_DIR"
)

"$SERVER_BIN" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
SERVER_PID=$!

wait $SERVER_PID