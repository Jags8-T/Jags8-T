"""Analytics agents for laboratory dashboard."""
from __future__ import annotations

from typing import Iterable

from .data_ingestion import LabResult


def compute_pass_fail_rate(results: Iterable[LabResult]) -> float:
    """Compute the pass rate for provided lab results.

    Args:
        results: An iterable of :class:`LabResult` instances.

    Returns:
        The fraction of tests that passed as a float between 0 and 1. If no
        results are provided, ``0.0`` is returned.
    """

    results = list(results)
    if not results:
        return 0.0

    passed = sum(1 for r in results if r.passed)
    return passed / len(results)
