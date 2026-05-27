#!/bin/sh
set -e

: "${FRONTEND_PORT:?}"

cd /app/cobalt/frontend

npm install
exec npm run dev -- --port "$FRONTEND_PORT" --host