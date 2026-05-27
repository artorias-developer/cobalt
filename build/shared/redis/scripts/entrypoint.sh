#!/bin/sh
set -e

if [ -n "$REDIS_PASSWORD" ]; then
  exec redis-server --save "" --appendonly no --requirepass "$REDIS_PASSWORD"
else
  exec redis-server --save "" --appendonly no
fi
