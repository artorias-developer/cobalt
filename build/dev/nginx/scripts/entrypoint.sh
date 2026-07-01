#!/bin/sh
set -e

: "${NGINX_PORT:?}"
: "${BACKEND_HOST:?}"
: "${BACKEND_PORT:?}"
: "${FRONTEND_HOST:?}"
: "${FRONTEND_PORT:?}"
: "${APP_DOMAIN:?}"

BACKEND_UPSTREAM_BLOCK="server $BACKEND_HOST:$BACKEND_PORT;"
FRONTEND_UPSTREAM_BLOCK="server $FRONTEND_HOST:$FRONTEND_PORT;"

SAFE_DOMAIN=$(echo "$APP_DOMAIN" | tr ':' '_')

sed "
s|\$BACKEND_UPSTREAM|$BACKEND_UPSTREAM_BLOCK|g;
s|\$FRONTEND_UPSTREAM|$FRONTEND_UPSTREAM_BLOCK|g;
s|\$NGINX_PORT|$NGINX_PORT|g;
s|\$SSL_CERT_FILE|$SAFE_DOMAIN.crt|g;
s|\$SSL_KEY_FILE|$SAFE_DOMAIN.key|g
" /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -g 'daemon off;'
