FROM node:22-alpine as builder

WORKDIR /app

COPY cobalt/frontend/package*.json ./
RUN npm install

COPY cobalt/frontend ./
RUN npm run build


FROM alpine:latest

WORKDIR /frontend-dist

COPY --from=builder /app/dist ./
