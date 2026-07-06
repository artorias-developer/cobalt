#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_ROOT="${SERVER_ROOT:-/opt/cobalt_server}"
SERVER_FIFO="${SERVER_FIFO:-/tmp/cobalt_server_fifo}"

SERVER_JAR="$SERVER_ROOT/fabric-server.jar"
LOG4J_CONFIG="$SERVER_ROOT/log4j2.xml"

SERVER_PID=""

function stop_server() {
    if [ -p "$SERVER_FIFO" ] && [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "stop" > "$SERVER_FIFO" 2>/dev/null

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

rm -f "$SERVER_FIFO"
mkfifo "$SERVER_FIFO"

sleep infinity > "$SERVER_FIFO" &
FIFO_HOLDER_PID=$!

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# nogui
SERVER_ARGS=(
    nogui
)

if [ -f "$LOG4J_CONFIG" ]; then
    export JAVA_TOOL_OPTIONS="-Dlog4j.configurationFile=$LOG4J_CONFIG"
fi

java -jar "$SERVER_JAR" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
SERVER_PID=$!

wait $SERVER_PID