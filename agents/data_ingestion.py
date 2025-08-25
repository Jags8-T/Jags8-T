"""Data ingestion agents for laboratory dashboard.

This module provides utilities to simulate pulling data from laboratory
instruments or LIMS systems. In a production environment these functions
would connect to external services or databases. For this example we use
static data to keep the code self‑contained.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any, List, Union
import csv



@dataclass
class LabResult:
    """Represents a single lab test result."""

    sample_id: str
    test_name: str
    value: float
    passed: bool


def load_sample_results() -> List[LabResult]:
    """Return a small list of sample lab results.

    In a real deployment this function would pull records from a LIMS or
    instrument API. Here we return a static list for demonstration and
    testing purposes.
    """

    return [
        LabResult(sample_id="S1", test_name="PCR", value=35.0, passed=True),
        LabResult(sample_id="S2", test_name="PCR", value=40.2, passed=False),
        LabResult(sample_id="S3", test_name="PCR", value=33.5, passed=True),
        LabResult(sample_id="S4", test_name="PCR", value=38.1, passed=False),
    ]


def load_results_from_csv(source: Union[str, Path, IO[str]]) -> List[LabResult]:
    """Load lab results from a CSV file or file-like object.

    The CSV is expected to contain the columns ``sample_id``, ``test_name``,
    ``value`` and ``passed``. The ``passed`` column may be ``1``/``0`` or any
    case-insensitive representation of ``true``/``false``.
    """

    close_after = False
    if hasattr(source, "read"):
        fh = source  # type: ignore[assignment]
    else:
        fh = open(source, newline="")
        close_after = True

    try:
        reader = csv.DictReader(fh)
        results: List[LabResult] = []
        for row in reader:
            results.append(
                LabResult(
                    sample_id=row["sample_id"],
                    test_name=row["test_name"],
                    value=float(row["value"]),
                    passed=str(row["passed"]).strip().lower() in {"1", "true", "yes", "pass"},
                )
            )
        return results
    finally:
        if close_after:
            fh.close()


def load_results_from_db(conn: Any, query: str) -> List[LabResult]:
    """Load lab results using an existing DB-API connection.

    Args:
        conn: An open database connection implementing the Python DB-API
            (e.g. from ``sqlite3`` or ``psycopg2``).
        query: SQL query returning ``sample_id``, ``test_name``, ``value`` and
            ``passed`` columns.
    """

    cursor = conn.execute(query)
    rows = cursor.fetchall()
    return [
        LabResult(
            sample_id=row[0],
            test_name=row[1],
            value=float(row[2]),
            passed=bool(row[3]),
        )
        for row in rows
    ]
