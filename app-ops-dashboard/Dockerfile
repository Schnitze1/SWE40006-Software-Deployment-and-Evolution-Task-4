# ============================================================
# SWE40006 Task 4.3 — Ops Dashboard OPTIMISED Multi-Stage Dockerfile
# Stage 1 (builder): install dependencies into a virtualenv
# Stage 2 (runtime): copy only the venv + application source
# Result: smaller final image, no build tooling in production layer
# ============================================================

# ---------- STAGE 1: DEPENDENCY BUILDER ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install dependencies into an isolated virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- STAGE 2: MINIMAL RUNTIME ----------
FROM python:3.12-slim AS runtime

LABEL maintainer="Timothy Schnabel <105334128@student.swin.edu.au>"
LABEL description="SWE40006 Task 4.3 Simple Unit Converter"
LABEL version="1.0.0"
LABEL build.strategy="multi-stage"

# Runtime environment variables (defaults; overridable at docker run -e)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_TITLE="Unit Converter" \
    APP_ENV="production" \
    APP_PORT="8080" \
    APP_VERSION="1.0.0"

WORKDIR /app

# Copy the pre-built virtualenv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source
COPY main.py .

# Non-root user hardening
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=20s --timeout=4s --start-period=8s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1

# Uvicorn production ASGI server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}"]
