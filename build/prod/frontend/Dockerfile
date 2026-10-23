FROM node:22-alpine AS builder

WORKDIR /app

COPY cobalt/frontend/package*.json ./
RUN npm install

COPY cobalt/frontend ./

RUN --mount=type=bind,source=generated/prod/build/frontend/.env,target=/app/.env \
    set -a && . /app/.env && set +a && npm run build

FROM alpine:3.24.2

WORKDIR /

COPY --from=builder /app/dist /frontend-dist-src

CMD ["sh", "-c", "rm -rf /frontend-dist/* && cp -r /frontend-dist-src/. /frontend-dist/"]