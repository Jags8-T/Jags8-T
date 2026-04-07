"""Professional Streamlit demo for an agentic laboratory operations dashboard."""
from __future__ import annotations

import io
import sqlite3
from typing import List

import streamlit as st

from agents import ChatAgent, analytics, data_ingestion


st.set_page_config(page_title="AI Laboratory Command Center", layout="wide")
st.title("🧪 AI Laboratory Command Center")
st.caption("Agentic demo: multi-source ingestion, KPI analytics, alerting, and operations copilot.")


@st.cache_data(show_spinner=False)
def _load_sample() -> List[data_ingestion.LabResult]:
    return data_ingestion.load_sample_results()


source_mode = st.sidebar.radio(
    "Connection mode",
    ["Sample", "CSV upload", "JSON upload", "SQLite query", "Multi-source merge"],
    index=0,
)

results: List[data_ingestion.LabResult] = []

if source_mode == "Sample":
    results = _load_sample()

elif source_mode == "CSV upload":
    uploaded = st.sidebar.file_uploader("Upload results.csv", type="csv")
    if uploaded:
        text_stream = io.StringIO(uploaded.getvalue().decode("utf-8"))
        results = data_ingestion.load_results_from_csv(text_stream)

elif source_mode == "JSON upload":
    uploaded = st.sidebar.file_uploader("Upload results.json", type="json")
    if uploaded:
        text_stream = io.StringIO(uploaded.getvalue().decode("utf-8"))
        results = data_ingestion.load_results_from_json(text_stream)

elif source_mode == "SQLite query":
    db_path = st.sidebar.text_input("SQLite database path")
    default_query = (
        "SELECT sample_id, test_name, value, passed, measured_at, source_system, technician "
        "FROM results"
    )
    query = st.sidebar.text_area("SQL query", value=default_query, height=100)
    if db_path:
        conn = sqlite3.connect(db_path)
        try:
            results = data_ingestion.load_results_from_db(conn, query)
        except Exception as exc:  # pragma: no cover - streamlit display path
            st.error(f"Unable to load data: {exc}")
        finally:
            conn.close()

elif source_mode == "Multi-source merge":
    st.sidebar.write("Merge built-in sample with optional CSV and JSON payloads.")
    csv_upload = st.sidebar.file_uploader("Optional CSV", type="csv")
    json_upload = st.sidebar.file_uploader("Optional JSON", type="json")

    merged = [_load_sample()]
    if csv_upload:
        merged.append(data_ingestion.load_results_from_csv(io.StringIO(csv_upload.getvalue().decode("utf-8"))))
    if json_upload:
        merged.append(data_ingestion.load_results_from_json(io.StringIO(json_upload.getvalue().decode("utf-8"))))
    results = data_ingestion.merge_results(*merged)

metrics = analytics.compute_dashboard_metrics(results)
alerts = analytics.detect_alerts(results)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total tests", metrics.total_tests)
c2.metric("Pass rate", f"{metrics.pass_rate:.0%}")
c3.metric("Failures", metrics.failed_tests)
c4.metric("Source systems", metrics.unique_systems)

st.subheader("🚨 Monitoring Alerts")
for alert in alerts:
    if "within expected" in alert.lower():
        st.success(alert)
    else:
        st.warning(alert)

tab_overview, tab_records, tab_copilot = st.tabs(["Overview", "Records", "Ops Copilot"])

with tab_overview:
    st.markdown("#### Pass rate by test")
    rate_map = analytics.pass_rate_by_test(results)
    if rate_map:
        st.bar_chart({"pass_rate": rate_map})
    else:
        st.info("No records available.")

    st.markdown("#### Daily test volume")
    trend = analytics.daily_volume(results)
    if trend:
        st.line_chart({"volume": trend})
    else:
        st.info("No records available.")

with tab_records:
    st.markdown("#### Normalized result table")
    table = [
        {
            "sample_id": r.sample_id,
            "test_name": r.test_name,
            "value": r.value,
            "status": "PASS" if r.passed else "FAIL",
            "measured_at_utc": r.measured_at.isoformat(),
            "source_system": r.source_system,
            "technician": r.technician,
        }
        for r in results
    ]
    st.dataframe(table, use_container_width=True)

with tab_copilot:
    st.markdown("#### Ask the operations copilot")
    st.caption("Example: 'Give KPI summary', 'pass rate by test', 'daily volume trend', 'failed samples'.")
    agent = ChatAgent(results)
    query = st.text_input("Ask about current loaded records")
    if query:
        st.write(agent.answer(query))
