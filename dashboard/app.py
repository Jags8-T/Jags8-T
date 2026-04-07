"""Simple Streamlit dashboard showcasing lab analytics and chat agent."""
from __future__ import annotations

import sqlite3
from pathlib import Path
import streamlit as st

from agents import ChatAgent, analytics, data_ingestion


st.set_page_config(page_title="Lab Dashboard", layout="wide")
st.title("Laboratory Dashboard")

# Sidebar data source selection
source = st.sidebar.selectbox(
    "Data source", ["Sample data", "CSV file", "SQLite DB"], index=0
)

results: list[data_ingestion.LabResult] = []
if source == "Sample data":
    results = data_ingestion.load_sample_results()
elif source == "CSV file":
    uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded:
        results = data_ingestion.load_results_from_csv(uploaded)
    else:
        st.info("Upload a CSV file to load results")
elif source == "SQLite DB":
    db_path = st.sidebar.text_input("SQLite database path")
    if db_path and Path(db_path).exists():
        conn = sqlite3.connect(db_path)
        try:
            results = data_ingestion.load_results_from_db(
                conn, "SELECT sample_id, test_name, value, passed FROM results"
            )
        finally:
            conn.close()
    else:
        st.info("Enter path to a SQLite database containing a 'results' table")

pass_rate = analytics.compute_pass_fail_rate(results)

st.metric("Pass rate", f"{pass_rate:.0%}")

st.subheader("Results")
for r in results:
    st.write(
        f"Sample {r.sample_id} – {r.test_name}: value={r.value} | "
        f"{'PASS' if r.passed else 'FAIL'}"
    )

st.subheader("Chat with assistant")
agent = ChatAgent(results)
query = st.text_input("Ask a question about the data:")
if query:
    response = agent.answer(query)
    st.write(response)
