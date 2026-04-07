"""Data ingestion agents for the laboratory dashboard.

The helpers in this module focus on safe, explicit data normalization so the
rest of the agentic pipeline can work with a consistent data contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any, Iterable, List, Mapping, Union
import csv
import json


TRUTHY_VALUES = {"1", "true", "yes", "pass", "passed", "y"}
FALSY_VALUES = {"0", "false", "no", "fail", "failed", "n"}


@dataclass(frozen=True)
class LabResult:
    """Represents a normalized lab test result row."""

    sample_id: str
    test_name: str
    value: float
    passed: bool
    measured_at: datetime
    source_system: str
    technician: str = "unknown"



def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)

    normalized = str(value).strip().lower()
    if normalized in TRUTHY_VALUES:
        return True
    if normalized in FALSY_VALUES:
        return False
    raise ValueError(f"Unsupported boolean value: {value!r}")



def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif value in (None, ""):
        dt = datetime.now(timezone.utc)
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)



def _normalize_record(record: Mapping[str, Any], default_source: str = "unknown") -> LabResult:
    return LabResult(
        sample_id=str(record["sample_id"]),
        test_name=str(record["test_name"]),
        value=float(record["value"]),
        passed=_parse_bool(record["passed"]),
        measured_at=_parse_datetime(record.get("measured_at")),
        source_system=str(record.get("source_system") or default_source),
        technician=str(record.get("technician") or "unknown"),
    )



def load_sample_results() -> List[LabResult]:
    """Return realistic synthetic records for demo and tests."""

    rows = [
        {"sample_id": "S-1001", "test_name": "PCR", "value": 32.1, "passed": True, "measured_at": "2026-03-31T08:05:00Z", "source_system": "LIMS-A", "technician": "A. Patel"},
        {"sample_id": "S-1002", "test_name": "PCR", "value": 40.2, "passed": False, "measured_at": "2026-03-31T08:15:00Z", "source_system": "LIMS-A", "technician": "A. Patel"},
        {"sample_id": "S-1003", "test_name": "CBC", "value": 5.6, "passed": True, "measured_at": "2026-04-01T09:10:00Z", "source_system": "Analyzer-X", "technician": "J. Kim"},
        {"sample_id": "S-1004", "test_name": "CBC", "value": 3.8, "passed": False, "measured_at": "2026-04-01T09:25:00Z", "source_system": "Analyzer-X", "technician": "J. Kim"},
        {"sample_id": "S-1005", "test_name": "Chem7", "value": 0.91, "passed": True, "measured_at": "2026-04-02T11:00:00Z", "source_system": "LIS-B", "technician": "M. Stone"},
        {"sample_id": "S-1006", "test_name": "Chem7", "value": 1.22, "passed": False, "measured_at": "2026-04-02T11:20:00Z", "source_system": "LIS-B", "technician": "M. Stone"},
        {"sample_id": "S-1007", "test_name": "PCR", "value": 34.4, "passed": True, "measured_at": "2026-04-03T10:00:00Z", "source_system": "LIMS-A", "technician": "T. Singh"},
        {"sample_id": "S-1008", "test_name": "PCR", "value": 36.5, "passed": True, "measured_at": "2026-04-03T10:35:00Z", "source_system": "LIMS-A", "technician": "T. Singh"},
    ]
    return [_normalize_record(row) for row in rows]



def load_results_from_csv(source: Union[str, Path, IO[str]]) -> List[LabResult]:
    """Load lab results from a CSV file or file-like object.

    Required columns: sample_id, test_name, value, passed.
    Optional columns: measured_at, source_system, technician.
    """

    close_after = False
    if hasattr(source, "read"):
        fh = source  # type: ignore[assignment]
    else:
        fh = open(source, newline="")
        close_after = True

    try:
        reader = csv.DictReader(fh)
        return [_normalize_record(row, default_source="csv") for row in reader]
    finally:
        if close_after:
            fh.close()



def load_results_from_json(source: Union[str, Path, IO[str]]) -> List[LabResult]:
    """Load lab results from a JSON array."""

    close_after = False
    if hasattr(source, "read"):
        fh = source  # type: ignore[assignment]
    else:
        fh = open(source)
        close_after = True

    try:
        payload = json.load(fh)
        if not isinstance(payload, list):
            raise ValueError("JSON payload must be a list of result objects")
        return [_normalize_record(row, default_source="json") for row in payload]
    finally:
        if close_after:
            fh.close()



def load_results_from_db(conn: Any, query: str, source_system: str = "database") -> List[LabResult]:
    """Load lab results using an existing DB-API connection.

    Query must return at least: sample_id, test_name, value, passed. It may also
    return measured_at, source_system, technician in this exact order.
    """

    rows = conn.execute(query).fetchall()
    results: List[LabResult] = []
    for row in rows:
        record = {
            "sample_id": row[0],
            "test_name": row[1],
            "value": row[2],
            "passed": row[3],
            "measured_at": row[4] if len(row) > 4 else None,
            "source_system": row[5] if len(row) > 5 else source_system,
            "technician": row[6] if len(row) > 6 else "unknown",
        }
        results.append(_normalize_record(record, default_source=source_system))
    return results



def merge_results(*collections: Iterable[LabResult]) -> List[LabResult]:
    """Merge multiple result collections and return in chronological order."""

    merged: List[LabResult] = []
    for collection in collections:
        merged.extend(collection)
    return sorted(merged, key=lambda row: row.measured_at)
