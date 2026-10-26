FROM python:3.12.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /bin/uv

WORKDIR /app/cobalt/backend

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PYTHON_PREFERENCE=only-system \
    UV_PROJECT_ENVIRONMENT=/opt/venv

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY cobalt/backend/pyproject.toml cobalt/backend/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

FROM python:3.12.13-slim

LABEL managed_by=cobalt

WORKDIR /app
ENV PYTHONPATH=/app/cobalt/backend
ENV PATH=/opt/venv/bin:$PATH

RUN apt-get update && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY Makefile /app/Makefile
COPY cobalt/backend /app/cobalt/backend