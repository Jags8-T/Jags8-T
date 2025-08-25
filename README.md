# Laboratory Dashboard Demo

This repository contains a minimal example of an agent-based laboratory dashboard.

## Components
- `agents/data_ingestion.py`: provides sample data records.
- `agents/analytics.py`: computes simple analytics such as pass rate.
- `dashboard/app.py`: a small [Streamlit](https://streamlit.io) application demonstrating the dashboard UI.

## Running the Dashboard
Install the required dependency:

```bash
pip install streamlit
```

Then launch the dashboard:

```bash
streamlit run dashboard/app.py
```

The app will display sample lab results and a placeholder chat interface.
