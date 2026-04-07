# Laboratory Dashboard Demo

This repository contains a minimal example of an agent-based laboratory dashboard.

## Components
- `agents/data_ingestion.py`: utilities for loading lab results. Besides
  built-in sample data it can read from CSV files or any database that exposes
  a Python DB-API connection.
- `agents/analytics.py`: computes simple analytics such as pass rate.
- `agents/chat_agent.py`: lightweight rule-based chat agent able to answer
  simple questions about the loaded results.
- `dashboard/app.py`: a small [Streamlit](https://streamlit.io) application
  demonstrating the dashboard UI with selectable data sources and a chat pane
  backed by the local chat agent.

## Running the Dashboard
Install the required dependency:

```bash
pip install streamlit
```

Then launch the dashboard:

```bash
streamlit run dashboard/app.py
```

The app will display sample lab results by default. Use the sidebar to load
results from a CSV file or a SQLite database. The chat section uses a simple
rule-based agent that can report the overall pass rate or list all sample
results.
