FROM python:3.12.13-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY cobalt/backend/requirements.txt /app/cobalt/backend/requirements.txt

RUN pip install --upgrade pip && \
    pip install --user -r /app/cobalt/backend/requirements.txt

FROM python:3.12.13-slim

WORKDIR /app
ENV PYTHONPATH=/app/cobalt/backend
ENV PATH=/root/.local/bin:$PATH

RUN apt-get update && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local