"""One-command demo runner for the AI laboratory dashboard."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from typing import Any, Dict

from agents import ChatAgent, analytics, data_ingestion


def build_demo_report() -> Dict[str, Any]:
    """Build a deterministic demo report from sample data."""

    results = data_ingestion.load_sample_results()
    metrics = analytics.compute_dashboard_metrics(results)
    agent = ChatAgent(results)

    return {
        "metrics": asdict(metrics),
        "pass_rate_by_test": analytics.pass_rate_by_test(results),
        "daily_volume": analytics.daily_volume(results),
        "alerts": analytics.detect_alerts(results),
        "copilot_examples": {
            "summary": agent.answer("Give KPI summary"),
            "pass_rate_by_test": agent.answer("pass rate by test"),
            "failed_samples": agent.answer("list failed samples"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lab dashboard demo checks.")
    parser.add_argument(
        "--launch-ui",
        action="store_true",
        help="Launch Streamlit UI after printing demo report.",
    )
    args = parser.parse_args()

    report = build_demo_report()
    print("=== Demo Report ===")
    print(json.dumps(report, indent=2, sort_keys=True))

    if args.launch_ui:
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard/app.py",
            "--server.headless",
            "true",
        ]
        print("\nLaunching Streamlit:", " ".join(cmd))
        return subprocess.call(cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
