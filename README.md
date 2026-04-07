# AI Laboratory Dashboard (Agentic Demo)

This repository provides an **immediate-demo, production-style prototype** of an
agentic laboratory dashboard. It is designed to show how ingestion agents,
analytics agents, and an operations copilot can work together in one interface.

## What is included

- **Ingestion Agent (`agents/data_ingestion.py`)**
  - Normalizes records into a strict `LabResult` contract.
  - Supports multiple input systems:
    - Built-in synthetic sample data
    - CSV upload
    - JSON upload
    - SQL query over DB-API connection (e.g., SQLite)
  - Supports multi-source merge for combined operational views.

- **Analytics Agent (`agents/analytics.py`)**
  - Dashboard KPIs (test count, pass/fail counts, pass rate, source count).
  - Pass rate by test type.
  - Daily volume trend.
  - Rule-based alerts for high failure rates.

- **Ops Copilot Agent (`agents/chat_agent.py`)**
  - Deterministic, no external LLM required.
  - Handles common lab manager prompts:
    - KPI summary
    - Overall and per-test pass rate
    - Daily volume trend
    - Failing sample list

- **Streamlit Command Center (`dashboard/app.py`)**
  - Multi-mode source connections.
  - KPI cards + alert panel.
  - Overview charts and records table.
  - Embedded operations copilot pane.

## Quick start

```bash
pip install streamlit
streamlit run dashboard/app.py
```

Open the local Streamlit URL and start in **Sample** mode for an instant demo.

## Suggested live demo flow (5 minutes)

1. Launch dashboard in **Sample** mode and review KPI cards.
2. Show **Monitoring Alerts** and explain threshold-based checks.
3. Open **Overview** tab to review pass rate by test + daily volume trend.
4. Open **Records** tab to show normalized fields (timestamp/system/technician).
5. In **Ops Copilot**, ask:
   - `Give KPI summary`
   - `pass rate by test`
   - `daily volume trend`
   - `list failed samples`
6. Switch to **CSV upload** or **JSON upload** to demonstrate connector agility.

## Data contract

Minimum required fields:
- `sample_id`
- `test_name`
- `value`
- `passed`

Optional fields:
- `measured_at` (ISO datetime preferred)
- `source_system`
- `technician`

Missing timestamps default to current UTC for continuity.
