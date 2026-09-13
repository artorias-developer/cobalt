FROM node:22-alpine as builder

WORKDIR /app

COPY cobalt/frontend/package*.json ./
RUN npm install

COPY cobalt/frontend ./
COPY build/prod/frontend/.env ./.env

RUN set -a && . ./.env && set +a && npm run build

FROM alpine:latest

WORKDIR /

COPY --from=builder /app/dist /frontend-dist-src

CMD ["sh", "-c", "rm -rf /frontend-dist/* && cp -r /frontend-dist-src/. /frontend-dist/"]