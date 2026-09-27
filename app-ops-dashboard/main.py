"""
SWE40006 Portfolio Task 4.3 — Simple Unit Converter
A basic custom web application demonstrating environment-variable driven
configuration, multi-stage optimised Docker builds, and container networking.
"""

import os
import platform
import time
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# ---------------------------------------------------------------------------
# Environment-variable driven configuration
# ---------------------------------------------------------------------------
APP_TITLE = os.getenv("APP_TITLE", "Unit Converter")
APP_ENV = os.getenv("APP_ENV", "production")
APP_PORT = int(os.getenv("APP_PORT", "8080"))
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = time.time()

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body>
  <h1>{title}</h1>
  <p>Task 4.3 &mdash; custom web application with environment configuration.</p>

  <h2>Temperature Converter</h2>
  <form method="get" action="/">
    <label>Celsius: <input type="number" step="any" name="c" value="{c}"></label>
    <input type="submit" value="Convert">
  </form>
  {result}

  <hr>
  <h2>Runtime Configuration</h2>
  <table border="1" cellpadding="6">
    <tr><td>APP_TITLE</td><td>{title}</td></tr>
    <tr><td>APP_ENV</td><td>{env}</td></tr>
    <tr><td>APP_PORT</td><td>{port}</td></tr>
    <tr><td>APP_VERSION</td><td>{version}</td></tr>
    <tr><td>Host</td><td>{hostname}</td></tr>
    <tr><td>Uptime (seconds)</td><td>{uptime}</td></tr>
    <tr><td>Time (UTC)</td><td>{now}</td></tr>
  </table>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def dashboard(c: str = ""):
    result_html = ""
    if c != "":
        try:
            celsius = float(c)
            fahrenheit = celsius * 9 / 5 + 32
            kelvin = celsius + 273.15
            result_html = (
                f"<h3>Result</h3>"
                f"<p>{celsius} C = {fahrenheit:.2f} F</p>"
                f"<p>{celsius} C = {kelvin:.2f} K</p>"
            )
        except ValueError:
            result_html = "<p>Please enter a valid number.</p>"
    return PAGE.format(
        title=APP_TITLE,
        env=APP_ENV,
        version=APP_VERSION,
        port=APP_PORT,
        c=c,
        result=result_html,
        uptime=int(time.time() - START_TIME),
        hostname=platform.node(),
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "unit-converter",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@app.get("/api/config")
def config():
    return {
        "app_title": APP_TITLE,
        "app_env": APP_ENV,
        "app_port": APP_PORT,
        "app_version": APP_VERSION,
    }
