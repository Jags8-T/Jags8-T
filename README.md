# Laboratory Dashboard Demo

This repository contains a minimal example of an agent-based laboratory dashboard.

## Components
- `agents/data_ingestion.py`: utilities for loading lab results. Besides
  built-in sample data it can read from CSV files or any database that exposes
  a Python DB-API connection.
- `agents/analytics.py`: computes simple analytics such as pass rate.
- `dashboard/app.py`: a small [Streamlit](https://streamlit.io) application
  demonstrating the dashboard UI with selectable data sources.

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
results from a CSV file or a SQLite database. The chat section remains a
placeholder for future LLM-powered agents.
