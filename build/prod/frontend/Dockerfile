FROM node:22-alpine

WORKDIR /app

COPY cobalt/frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY cobalt/frontend ./

LABEL managed_by=cobalt