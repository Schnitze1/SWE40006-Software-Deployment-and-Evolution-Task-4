"""
SWE40006 Portfolio Task 4.2 — Simple Flask Calculator
A basic Flask web application used to demonstrate containerisation,
dependency management, port publication, and multi-host image distribution.
"""

from datetime import datetime, timezone
from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Simple Calculator</title>
</head>
<body>
  <h1>Simple Calculator</h1>
  <p>Task 4.2 &mdash; Python Flask application containerised with Docker.</p>
  <form method="get" action="/calculate">
    <label>First number: <input type="number" step="any" name="a" value="{{ a }}"></label><br><br>
    <label>Operator:
      <select name="op">
        <option value="+" {% if op == '+' %}selected{% endif %}>+</option>
        <option value="-" {% if op == '-' %}selected{% endif %}>-</option>
        <option value="*" {% if op == '*' %}selected{% endif %}>*</option>
        <option value="/" {% if op == '/' %}selected{% endif %}>/</option>
      </select>
    </label><br><br>
    <label>Second number: <input type="number" step="any" name="b" value="{{ b }}"></label><br><br>
    <input type="submit" value="Calculate">
  </form>
  {% if result is not none %}
    <h2>Result: {{ a }} {{ op }} {{ b }} = {{ result }}</h2>
  {% endif %}
  {% if error %}
    <h2>Error: {{ error }}</h2>
  {% endif %}
  <hr>
  <p>Service: flask-calculator | Port: 5000 | Time (UTC): {{ now }}</p>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        PAGE,
        a="",
        b="",
        op="+",
        result=None,
        error=None,
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/calculate")
def calculate():
    error = None
    result = None
    a_raw = request.args.get("a", "")
    b_raw = request.args.get("b", "")
    op = request.args.get("op", "+")
    try:
        a = float(a_raw)
        b = float(b_raw)
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                error = "Cannot divide by zero"
            else:
                result = a / b
        else:
            error = "Unknown operator"
    except ValueError:
        error = "Please enter valid numbers"
    return render_template_string(
        PAGE,
        a=a_raw,
        b=b_raw,
        op=op,
        result=result,
        error=error,
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "flask-calculator",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
