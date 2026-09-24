#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

STEAMCMD_LOG="/tmp/steamcmd_output.log"
MAX_ATTEMPTS=3

function run_steamcmd() {
    steamcmd.sh +@ShutdownOnFailedCommand 1 \
                +@sSteamCmdForcePlatformType linux \
                +force_install_dir "$SERVER_ROOT" \
                +login anonymous \
                +app_update "$APP_ID" validate \
                +quit 2>&1 | tee "$STEAMCMD_LOG"
}

function upgrade_succeeded() {
    grep -q "Success! App '${APP_ID}' fully installed." "$STEAMCMD_LOG"
}

function main() {
    for i in $(seq 1 "$MAX_ATTEMPTS"); do
        run_steamcmd

        if upgrade_succeeded; then
            echo "Upgrade successful."
            rm -f "$STEAMCMD_LOG"
            exit 0
        fi

        echo "Attempt $i failed, retrying..."
        sleep 5
    done

    rm -f "$STEAMCMD_LOG"
    echo "All attempts failed."
    exit 1
}

main