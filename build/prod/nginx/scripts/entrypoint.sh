#!/bin/sh
set -e

: "${NGINX_PORT:?}"
: "${BACKEND_HOST:?}"
: "${BACKEND_PORT:?}"
: "${APP_DOMAIN:?}"

APP_BASE_URL="${APP_BASE_URL:-}"

BACKEND_UPSTREAM_BLOCK="server $BACKEND_HOST:$BACKEND_PORT;"
SAFE_DOMAIN=$(echo "$APP_DOMAIN" | tr ':' '_')

mkdir -p /etc/nginx/generated

if [ -n "$APP_BASE_URL" ]; then
    FRONT_TEMPLATE="/etc/nginx/parts/front-with-base.template.conf"
else
    FRONT_TEMPLATE="/etc/nginx/parts/front-without-base.template.conf"
fi

sed "s|\$APP_BASE_URL|$APP_BASE_URL|g" "$FRONT_TEMPLATE" > /etc/nginx/generated/front.conf

sed "
s|\$BACKEND_UPSTREAM|$BACKEND_UPSTREAM_BLOCK|g;
s|\$NGINX_PORT|$NGINX_PORT|g;
s|\$SSL_CERT_FILE|$SAFE_DOMAIN.crt|g;
s|\$SSL_KEY_FILE|$SAFE_DOMAIN.key|g
" /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -g 'daemon off;'