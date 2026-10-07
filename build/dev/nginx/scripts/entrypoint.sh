#!/bin/sh
set -e

: "${NGINX_PORT:?}"
: "${BACKEND_HOST:?}"
: "${BACKEND_PORT:?}"
: "${FRONTEND_HOST:?}"
: "${FRONTEND_PORT:?}"
: "${APP_DOMAIN:?}"
: "${APP_BASE_URL:=}"

TEMPLATE="/etc/nginx/snippets/nginx.conf"
CONFIG="/etc/nginx/nginx.conf"

fill() {
    file="$1"
    shift

    tmp=$(mktemp)
    sed "$@" "$file" > "$tmp"
    cat "$tmp" > "$file"
    rm -f "$tmp"
}

BACKEND_UPSTREAM_BLOCK="server $BACKEND_HOST:$BACKEND_PORT;"
FRONTEND_UPSTREAM_BLOCK="server $FRONTEND_HOST:$FRONTEND_PORT;"

SAFE_DOMAIN=$(echo "$APP_DOMAIN" | tr ':' '_')

cp "$TEMPLATE" "$CONFIG"

fill "$CONFIG" "
s|\$BACKEND_UPSTREAM|$BACKEND_UPSTREAM_BLOCK|g;
s|\$FRONTEND_UPSTREAM|$FRONTEND_UPSTREAM_BLOCK|g;
s|\$NGINX_PORT|$NGINX_PORT|g;
s|\$APP_DOMAIN|$SAFE_DOMAIN|g;
s|\$APP_BASE_URL|$APP_BASE_URL|g
"

nginx -g 'daemon off;'