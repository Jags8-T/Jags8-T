"""Tests for data ingestion helpers."""
import csv
import io
import json
import sqlite3

from agents import data_ingestion


def test_load_results_from_csv(tmp_path):
    csv_path = tmp_path / "results.csv"
    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "sample_id",
                "test_name",
                "value",
                "passed",
                "measured_at",
                "source_system",
                "technician",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "sample_id": "S1",
                "test_name": "PCR",
                "value": "1.0",
                "passed": "1",
                "measured_at": "2026-04-01T00:00:00Z",
                "source_system": "CSV-LIMS",
                "technician": "Tech",
            }
        )

    results = data_ingestion.load_results_from_csv(csv_path)
    assert len(results) == 1
    assert results[0].source_system == "CSV-LIMS"


def test_load_results_from_json():
    payload = io.StringIO(
        json.dumps(
            [
                {
                    "sample_id": "S2",
                    "test_name": "CBC",
                    "value": 2.5,
                    "passed": "true",
                    "source_system": "JSON-LIMS",
                }
            ]
        )
    )
    results = data_ingestion.load_results_from_json(payload)
    assert results[0].passed is True


def test_load_results_from_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE results (sample_id TEXT, test_name TEXT, value REAL, passed INTEGER, measured_at TEXT, source_system TEXT, technician TEXT)"
    )
    conn.execute(
        "INSERT INTO results VALUES ('S1', 'PCR', 1.0, 1, '2026-04-01T00:00:00Z', 'DB-LIMS', 'Tech')"
    )
    conn.commit()

    results = data_ingestion.load_results_from_db(
        conn,
        "SELECT sample_id, test_name, value, passed, measured_at, source_system, technician FROM results",
    )
    conn.close()

    assert results[0].source_system == "DB-LIMS"


def test_merge_results_keeps_chronological_order():
    sample = data_ingestion.load_sample_results()
    merged = data_ingestion.merge_results(sample[4:], sample[:4])
    assert merged[0].measured_at <= merged[-1].measured_at
