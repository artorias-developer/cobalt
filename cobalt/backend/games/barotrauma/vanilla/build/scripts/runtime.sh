#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

SERVER_ROOT="${SERVER_ROOT:-/opt/cobalt_server}"
SERVER_FIFO="${SERVER_FIFO:-/tmp/cobalt_server_fifo}"

SESSION_NAME="cobalt_server"
DONE_CHANNEL="${SESSION_NAME}_done"

LOG_PIPE="/tmp/cobalt_server_log"
SERVER_BIN="$SERVER_ROOT/DedicatedServer"

FIFO_READER_PID=""
LOG_TAIL_PID=""
WAIT_BG_PID=""

function stop_server() {
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "quit" > "$SERVER_FIFO" 2>/dev/null

        for i in $(seq 1 60); do
            tmux has-session -t "$SESSION_NAME" 2>/dev/null || break
            sleep 1
        done

        if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
            tmux kill-session -t "$SESSION_NAME" 2>/dev/null
        fi
    fi

    [ -n "$FIFO_READER_PID" ] && kill "$FIFO_READER_PID" 2>/dev/null
    [ -n "$LOG_TAIL_PID" ] && kill "$LOG_TAIL_PID" 2>/dev/null
    [ -n "$WAIT_BG_PID" ] && kill "$WAIT_BG_PID" 2>/dev/null

    tmux kill-server 2>/dev/null

    rm -f "$SERVER_FIFO" "$LOG_PIPE"
    exit 0
}

function setup_pipes() {
    rm -f "$SERVER_FIFO" "$LOG_PIPE"
    mkfifo "$SERVER_FIFO"
    mkfifo "$LOG_PIPE"
}

function start_server_session() {
    local server_args=()

    tmux -f /dev/null new-session -d -s "$SESSION_NAME" -x 220 -y 50 \
        "$SERVER_BIN ${server_args[*]}; tmux wait-for -S $DONE_CHANNEL"

    local pane_tty
    pane_tty=$(tmux display-message -p -t "$SESSION_NAME" '#{pane_tty}')
    stty -echo -F "$pane_tty" 2>/dev/null || true

    tmux pipe-pane -o -t "$SESSION_NAME" "cat >> $LOG_PIPE"
}

function start_log_filter() {
    local esc=$'\033'

    local -a filters=(
        -e "s/${esc}\[[0-9;?]*[A-Za-z]//g"
        -e "s/${esc}[=>]//g"
        -e "s/^[[:space:]]+//"
        -e "s|^\[[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\] ?||"
        -e "s/[[:space:]]+$//"
        -e "/^$/d"
    )

    sed -u -E "${filters[@]}" "$LOG_PIPE" | stdbuf -oL uniq &
    LOG_TAIL_PID=$!
}

function start_fifo_reader() {
    (
        while true; do
            if IFS= read -r line < "$SERVER_FIFO"; then
                line="${line%$'\r'}"
                [ -z "$line" ] && continue
                tmux send-keys -t "$SESSION_NAME" -l -- "$line"$'\r'
            fi
        done
    ) &
    FIFO_READER_PID=$!
}

function main() {
    trap stop_server SIGINT SIGTERM

    cd "$SERVER_ROOT"
    setup_pipes
    start_server_session
    start_log_filter
    start_fifo_reader

    tmux wait-for "$DONE_CHANNEL" &
    WAIT_BG_PID=$!
    wait "$WAIT_BG_PID"

    stop_server
}

main