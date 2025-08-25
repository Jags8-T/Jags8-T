"""Tests for data ingestion helpers."""
import csv
import sqlite3

from agents import data_ingestion


def test_load_results_from_csv(tmp_path):
    csv_path = tmp_path / "results.csv"
    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["sample_id", "test_name", "value", "passed"]
        )
        writer.writeheader()
        writer.writerow(
            {
                "sample_id": "S1",
                "test_name": "PCR",
                "value": "1.0",
                "passed": "1",
            }
        )

    results = data_ingestion.load_results_from_csv(csv_path)
    assert results == [
        data_ingestion.LabResult("S1", "PCR", 1.0, True)
    ]


def test_load_results_from_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE results (sample_id TEXT, test_name TEXT, value REAL, passed INTEGER)"
    )
    conn.execute(
        "INSERT INTO results VALUES ('S1', 'PCR', 1.0, 1)"
    )
    conn.commit()

    results = data_ingestion.load_results_from_db(
        conn, "SELECT sample_id, test_name, value, passed FROM results"
    )
    conn.close()

    assert results == [data_ingestion.LabResult("S1", "PCR", 1.0, True)]

