#!/bin/sh
set -e

: "${NGINX_PORT:?}"
: "${BACKEND_HOST:?}"
: "${BACKEND_PORT:?}"
: "${APP_DOMAIN:?}"

APP_BASE_URL="${APP_BASE_URL:-}"

SNIPPETS="/etc/nginx/snippets"
CONFIG="/etc/nginx/nginx.conf"
FRONT_CONFIG="/etc/nginx/generated/front.conf"

fill() {
    file="$1"
    shift

    tmp=$(mktemp)
    sed "$@" "$file" > "$tmp"
    cat "$tmp" > "$file"
    rm -f "$tmp"
}

BACKEND_UPSTREAM_BLOCK="server $BACKEND_HOST:$BACKEND_PORT;"
SAFE_DOMAIN=$(echo "$APP_DOMAIN" | tr ':' '_')

mkdir -p /etc/nginx/generated

if [ -n "$APP_BASE_URL" ]; then
    FRONT_TEMPLATE="$SNIPPETS/front/with-base.conf"
else
    FRONT_TEMPLATE="$SNIPPETS/front/without-base.conf"
fi

cp "$FRONT_TEMPLATE" "$FRONT_CONFIG"
fill "$FRONT_CONFIG" "
s|\$APP_BASE_URL|$APP_BASE_URL|g
"

cp "$SNIPPETS/nginx.conf" "$CONFIG"
fill "$CONFIG" "
s|\$BACKEND_UPSTREAM|$BACKEND_UPSTREAM_BLOCK|g;
s|\$NGINX_PORT|$NGINX_PORT|g;
s|\$APP_DOMAIN|$SAFE_DOMAIN|g
"

nginx -g 'daemon off;'