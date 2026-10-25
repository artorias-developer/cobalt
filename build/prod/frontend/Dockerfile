FROM node:22-alpine

LABEL managed_by=cobalt

WORKDIR /app

COPY cobalt/frontend/package*.json ./
RUN npm install

COPY cobalt/frontend ./