"""Deterministic operations copilot for the laboratory dashboard."""
from __future__ import annotations

from typing import Iterable, List

from .analytics import compute_dashboard_metrics, daily_volume, pass_rate_by_test
from .data_ingestion import LabResult


class ChatAgent:
    """Answer practical operations questions from loaded lab results."""

    def __init__(self, results: Iterable[LabResult]):
        self.results: List[LabResult] = list(results)

    def answer(self, query: str) -> str:
        q = query.strip().lower()
        if not self.results:
            return "No data is currently loaded. Connect CSV, JSON, or database data first."

        metrics = compute_dashboard_metrics(self.results)

        if any(token in q for token in ["summary", "kpi", "overview"]):
            return (
                f"Processed {metrics.total_tests} tests across {metrics.unique_samples} samples and "
                f"{metrics.unique_systems} systems. Pass rate is {metrics.pass_rate:.0%}."
            )

        if "pass rate" in q and "test" in q:
            per_test = pass_rate_by_test(self.results)
            return "\n".join(f"{name}: {rate:.0%}" for name, rate in sorted(per_test.items()))

        if "pass rate" in q:
            return f"The overall pass rate is {metrics.pass_rate:.0%}."

        if "volume" in q or "daily" in q or "trend" in q:
            counts = daily_volume(self.results)
            return "\n".join(f"{day}: {count} tests" for day, count in counts.items())

        if "fail" in q and "sample" in q:
            failed = [r for r in self.results if not r.passed]
            if not failed:
                return "No failing samples in the loaded dataset."
            return "\n".join(
                f"{r.sample_id} ({r.test_name}) from {r.source_system}"
                for r in failed
            )

        return (
            "I can provide KPI summary, overall/per-test pass rate, daily volume trend, "
            "or list failing samples."
        )
