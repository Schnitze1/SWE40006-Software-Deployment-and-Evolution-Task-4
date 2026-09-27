# ============================================================
# SWE40006 Task 4.2 — Flask Portal Dockerfile
# Multi-purpose Python runtime image for the Deployment Portal
# ============================================================

# 1. Base image: official slim Python 3.12 runtime
FROM python:3.12-slim

# 2. Image metadata (OCI labels)
LABEL maintainer="Timothy Schnabel <105334128@student.swin.edu.au>"
LABEL description="SWE40006 Task 4.2 Flask Simple Calculator"
LABEL version="1.0"

# 3. Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

# 4. Set the working directory inside the container
WORKDIR /usr/src/app

# 5. Copy and install Python dependencies first (layer caching optimisation)
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy the application source code
COPY . .

# 7. Create a non-root user for container security hardening
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /usr/src/app
USER appuser

# 8. Declare the listening port
EXPOSE 5000

# 9. Health check against the /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

# 10. Default command — run with Gunicorn for production-grade process management
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
