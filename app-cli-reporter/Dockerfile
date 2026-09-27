# ============================================================
# SWE40006 Task 4.4 — Non-Web CLI Tool Dockerfile (best practices)
# Ephemeral batch container: no EXPOSE, no long-running process,
# explicit volumes, non-root user, deterministic exit codes
# ============================================================

FROM python:3.12-slim

LABEL maintainer="Timothy Schnabel <105334128@student.swin.edu.au>"
LABEL description="SWE40006 Task 4.4 Log Analytics CLI Reporter"
LABEL version="1.0.0"
LABEL workload.type="batch-cli"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REPORT_INPUT=/data/input/app.log \
    REPORT_OUTPUT=/data/output/report.json \
    REPORT_FORMAT=json

WORKDIR /app

COPY log_reporter.py .

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /data/input /data/output \
    && chown -R appuser:appuser /data /app
USER appuser

# Declare persistent data locations for host bind mounts / named volumes
VOLUME ["/data/input", "/data/output"]

# No EXPOSE — this is not a network service
ENTRYPOINT ["python", "log_reporter.py"]
CMD ["--input", "/data/input/app.log", "--output", "/data/output/report.json", "--format", "json"]
