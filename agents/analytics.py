"""Analytics agents for laboratory dashboard."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List

from .data_ingestion import LabResult


@dataclass(frozen=True)
class DashboardMetrics:
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    unique_samples: int
    unique_systems: int



def compute_pass_fail_rate(results: Iterable[LabResult]) -> float:
    results = list(results)
    if not results:
        return 0.0
    passed = sum(1 for r in results if r.passed)
    return passed / len(results)



def compute_dashboard_metrics(results: Iterable[LabResult]) -> DashboardMetrics:
    rows = list(results)
    total = len(rows)
    passed = sum(1 for r in rows if r.passed)
    failed = total - passed
    return DashboardMetrics(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        pass_rate=(passed / total) if total else 0.0,
        unique_samples=len({r.sample_id for r in rows}),
        unique_systems=len({r.source_system for r in rows}),
    )



def pass_rate_by_test(results: Iterable[LabResult]) -> Dict[str, float]:
    grouped: Dict[str, List[LabResult]] = defaultdict(list)
    for row in results:
        grouped[row.test_name].append(row)
    return {test_name: compute_pass_fail_rate(rows) for test_name, rows in grouped.items()}



def daily_volume(results: Iterable[LabResult]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for row in results:
        counts[row.measured_at.date().isoformat()] += 1
    return dict(sorted(counts.items()))



def detect_alerts(results: Iterable[LabResult], fail_rate_threshold: float = 0.4) -> List[str]:
    alerts: List[str] = []
    rows = list(results)
    if not rows:
        return ["No records loaded. Connect a source to enable monitoring."]

    metrics = compute_dashboard_metrics(rows)
    overall_fail_rate = 1.0 - metrics.pass_rate
    if overall_fail_rate > fail_rate_threshold:
        alerts.append(
            f"High failure rate detected ({overall_fail_rate:.0%}), above threshold {fail_rate_threshold:.0%}."
        )

    per_test = pass_rate_by_test(rows)
    for test_name, rate in per_test.items():
        if (1.0 - rate) > fail_rate_threshold:
            alerts.append(f"{test_name} has elevated failures at {(1.0 - rate):.0%}.")

    if not alerts:
        alerts.append("All monitored KPIs are within expected thresholds.")

    return alerts
