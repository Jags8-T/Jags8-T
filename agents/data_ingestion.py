"""Data ingestion agents for laboratory dashboard.

This module provides utilities to simulate pulling data from laboratory
instruments or LIMS systems. In a production environment these functions
would connect to external services or databases. For this example we use
static data to keep the code self‑contained.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


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
