#!/bin/sh
set -e

: "${NGINX_PORT:?}"
: "${BACKEND_HOST:?}"
: "${BACKEND_PORT:?}"

BACKEND_UPSTREAM_BLOCK="server $BACKEND_HOST:$BACKEND_PORT;"

sed "
s|\$BACKEND_UPSTREAM|$BACKEND_UPSTREAM_BLOCK|g;
s|\$NGINX_PORT|$NGINX_PORT|g
" /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -g 'daemon off;'
