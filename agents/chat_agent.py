"""Simple rule-based chat agent for the laboratory dashboard."""
from __future__ import annotations

from typing import Iterable, List

from .data_ingestion import LabResult
from .analytics import compute_pass_fail_rate


class ChatAgent:
    """Answer basic natural language questions about lab results.

    The implementation is intentionally lightweight and deterministic so it can
    run in limited environments without requiring external LLM services.
    Currently it understands questions about overall pass rate and listing all
    sample results.
    """

    def __init__(self, results: Iterable[LabResult]):
        self.results: List[LabResult] = list(results)

    def answer(self, query: str) -> str:
        """Return a response for ``query``.

        The matching is intentionally simple and based on lowercase keyword
        checks to keep the demo self‑contained.
        """

        q = query.strip().lower()
        if not self.results:
            return "No data is currently loaded."

        if "pass rate" in q:
            rate = compute_pass_fail_rate(self.results)
            return f"The pass rate is {rate:.0%}."

        if "list" in q and "sample" in q:
            lines = [
                f"{r.sample_id} – {r.test_name}: {r.value} ({'PASS' if r.passed else 'FAIL'})"
                for r in self.results
            ]
            return "\n".join(lines)

        return (
            "I can tell you the pass rate or list sample results. "
            "Try asking 'What is the pass rate?'"
        )

