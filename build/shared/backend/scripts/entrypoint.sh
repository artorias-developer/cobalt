#!/bin/sh
set -e

echo "$(date '+%Y-%m-%d %H:%M:%S') INFO Running migrations..."
make a:u

echo "$(date '+%Y-%m-%d %H:%M:%S') INFO Starting application..."
exec python /app/cobalt/backend/main.py