"""Simple Streamlit dashboard showcasing lab analytics and chat agent."""
from __future__ import annotations

import streamlit as st

from agents import analytics, data_ingestion


st.set_page_config(page_title="Lab Dashboard", layout="wide")
st.title("Laboratory Dashboard")

results = data_ingestion.load_sample_results()
pass_rate = analytics.compute_pass_fail_rate(results)

st.metric("Pass rate", f"{pass_rate:.0%}")

st.subheader("Results")
for r in results:
    st.write(
        f"Sample {r.sample_id} – {r.test_name}: value={r.value} | "
        f"{'PASS' if r.passed else 'FAIL'}"
    )

st.subheader("Chat with assistant")
query = st.text_input("Ask a question about the data:")
if query:
    st.write(
        "This demo does not connect to a real language model, but a future "
        "implementation could route this query to an LLM-powered agent."
    )
