#!/bin/bash

# Copyright (C) 2026 Artorias
# Author: Artorias
# Repository: https://github.com/artorias-developer/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u

INSTALLER_SRC="/installer_src"
STEAMCMD_LOG="/tmp/steamcmd_output.log"
MAX_ATTEMPTS=3

function sync_files() {
    rsync -a \
        --exclude 'serversettings.example.xml' \
        --exclude 'installer.sh' \
        "$INSTALLER_SRC/." .
}

function run_steamcmd() {
    steamcmd.sh +@ShutdownOnFailedCommand 1 \
                +@sSteamCmdForcePlatformType linux \
                +force_install_dir "$SERVER_ROOT" \
                +login anonymous \
                +app_update "$APP_ID" validate \
                +quit 2>&1 | tee "$STEAMCMD_LOG"
}

function install_succeeded() {
    grep -q "Success! App '${APP_ID}' fully installed." "$STEAMCMD_LOG"
}

function setup_config() {
    cp -f "$INSTALLER_SRC/serversettings.example.xml" "$SERVER_ROOT/serversettings.xml"
    sed -i "s|{SERVER_PORT}|$SERVER_PORT|g" "$SERVER_ROOT/serversettings.xml"
    sed -i "s|{QUERY_PORT}|$QUERY_PORT|g" "$SERVER_ROOT/serversettings.xml"
}

function main() {
    sync_files

    for i in $(seq 1 "$MAX_ATTEMPTS"); do
        run_steamcmd

        if install_succeeded; then
            echo "Install successful."
            rm -f "$STEAMCMD_LOG"
            setup_config
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