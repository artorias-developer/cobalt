#!/bin/sh
set -e

cd /app
npm run build

rm -rf /frontend-dist/*
cp -r dist/. /frontend-dist/