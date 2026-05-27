#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_ROOT="${SERVER_ROOT:-/opt/cobalt_server}"
SERVER_FIFO="${SERVER_FIFO:-/tmp/cobalt_server_fifo}"

SERVER_BIN="$SERVER_ROOT/bin/dontstarve_dedicated_server_nullrenderer"
CLUSTER_ROOT="$SERVER_ROOT/DoNotStarveTogether/cluster"
CLUSTER_INI="$CLUSTER_ROOT/cluster.ini"

SERVER_PID=""

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

trap stop_server SIGINT SIGTERM

if [ -f "$CLUSTER_INI" ]; then
    sed -i "s|{CONTAINER_NAME}|$CONTAINER_NAME|g" "$CLUSTER_INI"
    sed -i "s|{CLUSTER_KEY}|$CLUSTER_KEY|g" "$CLUSTER_INI"
fi

rm -f "$SERVER_FIFO"
mkfifo "$SERVER_FIFO"

sleep infinity > "$SERVER_FIFO" &
FIFO_HOLDER_PID=$!

cd "$SERVER_ROOT/bin"

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

"$SERVER_BIN" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
SERVER_PID=$!

wait $SERVER_PID