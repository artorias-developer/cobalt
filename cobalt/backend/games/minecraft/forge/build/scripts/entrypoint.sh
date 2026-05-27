#!/bin/bash

# Copyright (C) 2026 ArtoriasCode
# Author: ArtoriasCode
# Repository: https://github.com/ArtoriasCode/cobalt
# SPDX-License-Identifier: AGPL-3.0-or-later

SERVER_ROOT="${SERVER_ROOT:-/opt/cobalt_server}"
SERVER_FIFO="${SERVER_FIFO:-/tmp/cobalt_server_fifo}"
LOADER_MODE="${LOADER_MODE:-latest}"
TWEAK_CLASS="${TWEAK_CLASS:-net}"

LOG4J_CONFIG="$SERVER_ROOT/log4j2.xml"
RUN_SCRIPT="$SERVER_ROOT/run.sh"
MC_SERVER_JAR="$SERVER_ROOT/minecraft_server.jar"

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

if [ "$LOADER_MODE" = "latest" ]; then
    if [ ! -f "$RUN_SCRIPT" ]; then
        echo "ERROR: run.sh not found in $SERVER_ROOT"
        exit 1
    fi

    "$RUN_SCRIPT" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
    SERVER_PID=$!
else
    UNIVERSAL_JAR=$(find "$SERVER_ROOT" -maxdepth 1 \( -name "*universal*.jar" -o -name "*forge*.jar" \) | head -n 1)

    if [ -z "$UNIVERSAL_JAR" ]; then
        echo "ERROR: No Forge jar found in $SERVER_ROOT"
        exit 1
    fi

    LEGACY_MC=$(find "$SERVER_ROOT" -maxdepth 1 -name "minecraft_server*.jar" | head -n 1)

    if [ -z "$LEGACY_MC" ]; then
        echo "ERROR: No minecraft_server jar found in $SERVER_ROOT"
        exit 1
    fi

    if [ ! -f "$MC_SERVER_JAR" ]; then
        cp "$LEGACY_MC" "$MC_SERVER_JAR"
    fi

    if [ "$LOADER_MODE" = "legacy" ]; then
        java -jar "$UNIVERSAL_JAR" "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
        SERVER_PID=$!
    else
        LAUNCHWRAPPER=$(find "$SERVER_ROOT/libraries" -name "*launchwrapper*.jar" 2>/dev/null | head -n 1)

        if [ -z "$LAUNCHWRAPPER" ]; then
            echo "ERROR: No launchwrapper jar found in $SERVER_ROOT/libraries"
            exit 1
        fi

        if [ "$TWEAK_CLASS" = "cpw" ]; then
            TWEAK="cpw.mods.fml.common.launcher.FMLServerTweaker"
        else
            TWEAK="net.minecraftforge.fml.common.launcher.FMLServerTweaker"
        fi

        java -cp "$MC_SERVER_JAR:$UNIVERSAL_JAR:$LAUNCHWRAPPER" \
            net.minecraft.launchwrapper.Launch \
            --tweakClass "$TWEAK" \
            "${SERVER_ARGS[@]}" < "$SERVER_FIFO" &
        SERVER_PID=$!
    fi
fi

wait $SERVER_PID