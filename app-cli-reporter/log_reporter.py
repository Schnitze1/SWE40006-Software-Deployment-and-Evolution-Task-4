"""
SWE40006 Portfolio Task 4.4 — Log Analytics CLI Reporter
A non-web command-line data-processing tool. Reads container/host log
line data from a mounted volume, computes summary statistics, and writes
a formatted report to an output volume. Demonstrates Docker best practices
for batch/CLI workloads: ephemeral containers, host bind mounts, exit-code
based lifecycle, and structured stdout logging.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="log-reporter",
        description="Analyse log files and emit a structured deployment report.",
    )
    parser.add_argument(
        "--input",
        default=os.getenv("REPORT_INPUT", "/data/input/app.log"),
        help="Path to the input log file (default: /data/input/app.log)",
    )
    parser.add_argument(
        "--output",
        default=os.getenv("REPORT_OUTPUT", "/data/output/report.json"),
        help="Path for the generated report (default: /data/output/report.json)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default=os.getenv("REPORT_FORMAT", "json"),
        help="Output format for the report",
    )
    return parser.parse_args()


def analyse(lines: list[str]) -> dict:
    level_counts: Counter[str] = Counter()
    keyword_hits: Counter[str] = Counter()
    total = 0
    errors: list[str] = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        total += 1
        upper = line.upper()
        for level in LEVELS:
            if level in upper:
                level_counts[level] += 1
                break
        for keyword in ("docker", "deploy", "build", "push", "pull", "container"):
            if keyword in line.lower():
                keyword_hits[keyword] += 1
        if "ERROR" in upper or "CRITICAL" in upper:
            errors.append(line)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool": "log-reporter",
        "version": "1.0.0",
        "input_path": str(os.getenv("REPORT_INPUT", "/data/input/app.log")),
        "total_lines_processed": total,
        "level_counts": dict(level_counts),
        "keyword_hits": dict(keyword_hits),
        "error_line_count": len(errors),
        "sample_errors": errors[:5],
    }


def render_text(report: dict) -> str:
    lines = [
        "=" * 60,
        "  LOG ANALYTICS REPORT — SWE40006 Task 4.4",
        "=" * 60,
        f"  Generated (UTC) : {report['generated_at_utc']}",
        f"  Tool / Version  : {report['tool']} v{report['version']}",
        f"  Input path      : {report['input_path']}",
        f"  Lines processed : {report['total_lines_processed']}",
        f"  Error lines     : {report['error_line_count']}",
        "",
        "  Log level distribution:",
    ]
    for level in LEVELS:
        count = report["level_counts"].get(level, 0)
        bar = "#" * min(count, 40)
        lines.append(f"    {level:<10} {count:>5}  {bar}")
    lines.append("")
    lines.append("  Keyword frequency:")
    for key, count in sorted(report["keyword_hits"].items()):
        lines.append(f"    {key:<12} {count:>5}")
    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    print(f"[log-reporter] starting analysis at {datetime.now(timezone.utc).isoformat()}")
    print(f"[log-reporter] input  = {input_path}")
    print(f"[log-reporter] output = {output_path}")
    print(f"[log-reporter] format = {args.format}")

    if not input_path.exists():
        print(f"[log-reporter] ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2

    lines = input_path.read_text(encoding="utf-8", errors="replace").splitlines()
    report = analyse(lines)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
    else:
        text = render_text(report)
        output_path.write_text(text, encoding="utf-8")
        print(text)

    print(f"[log-reporter] report written successfully to {output_path}")
    print(f"[log-reporter] completed with exit code 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
