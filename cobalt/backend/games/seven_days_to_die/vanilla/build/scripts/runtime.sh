#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_BIN="$SERVER_ROOT/7DaysToDieServer.x86_64"
SERVER_CONFIG="$SERVER_ROOT/serverconfig.xml"
LOG_FILE="$SERVER_ROOT/output_log__`date +%Y-%m-%d__%H-%M-%S`.txt"

TELNET_IN="/tmp/cobalt_telnet_in"

SERVER_PID=""
FIFO_READER_PID=""
TELNET_HOLDER_PID=""
TELNET_PID=""
TELNET_MANAGER_PID=""

# Add any additional server arguments here.
# WARNING: The following arguments are already handled and should not be added:
# -configfile
# -batchmode
# -nographics
# -dedicated
SERVER_ARGS=(
    -configfile="$SERVER_CONFIG"
    -logfile "$LOG_FILE"
    -quit
    -batchmode
    -nographics
    -dedicated
)

function connect_telnet() {
    while true; do
        if [ -n "$TELNET_PID" ] && kill -0 "$TELNET_PID" 2>/dev/null; then
            kill "$TELNET_PID" 2>/dev/null
        fi

        if [ -n "$TELNET_HOLDER_PID" ] && kill -0 "$TELNET_HOLDER_PID" 2>/dev/null; then
            kill "$TELNET_HOLDER_PID" 2>/dev/null
        fi

        rm -f "$TELNET_IN"
        mkfifo "$TELNET_IN"

        sleep infinity > "$TELNET_IN" &
        TELNET_HOLDER_PID=$!

        nc -q 0 127.0.0.1 8081 < "$TELNET_IN" &
        TELNET_PID=$!

        wait "$TELNET_PID" 2>/dev/null

        if ! kill -0 "$SERVER_PID" 2>/dev/null; then
            break
        fi

        echo "Telnet disconnected, reconnecting in 3s..."
        sleep 3
    done
}

function stop_server() {
    if [ -n "$TELNET_IN" ] && [ -p "$TELNET_IN" ]; then
        echo "shutdown" > "$TELNET_IN" 2>/dev/null

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

    if [ -n "$FIFO_READER_PID" ]; then
        kill "$FIFO_READER_PID" 2>/dev/null
    fi

    if [ -n "$TELNET_MANAGER_PID" ]; then
        kill "$TELNET_MANAGER_PID" 2>/dev/null
    fi

    if [ -n "$TELNET_HOLDER_PID" ]; then
        kill "$TELNET_HOLDER_PID" 2>/dev/null
    fi

    if [ -n "$TELNET_PID" ]; then
        kill "$TELNET_PID" 2>/dev/null
    fi

    rm -f "$SERVER_FIFO"
    rm -f "$TELNET_IN"
    exit 0
}

function setup_fifo() {
    rm -f "$SERVER_FIFO"
    mkfifo "$SERVER_FIFO"
}

function filter_log() {
    sed -u -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]+\.[0-9]+ [A-Z]{3} //'
}

function start_server() {
    cd "$SERVER_ROOT"
    rm -f output_log__*.txt

    "$SERVER_BIN" "${SERVER_ARGS[@]}" > >(filter_log) 2>&1 &
    SERVER_PID=$!
}

function wait_for_telnet() {
    echo "Waiting for Telnet to become available..."
    until nc -z 127.0.0.1 8081 2>/dev/null; do
        sleep 2
    done
    echo "Telnet is available, connecting..."
}

function start_telnet_manager() {
    connect_telnet &
    TELNET_MANAGER_PID=$!
}

function start_fifo_reader() {
    while true; do
        if read -r cmd < "$SERVER_FIFO"; then
            if [ -p "$TELNET_IN" ]; then
                echo "$cmd" > "$TELNET_IN"
            fi
        fi
    done &
    FIFO_READER_PID=$!
}

function main() {
    trap stop_server SIGINT SIGTERM

    setup_fifo
    start_server
    wait_for_telnet
    start_telnet_manager
    start_fifo_reader

    wait $SERVER_PID
}

main