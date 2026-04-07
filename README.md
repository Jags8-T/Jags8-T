# AI Laboratory Dashboard (Agentic Demo)

This repository provides an **immediate-demo, production-style prototype** of an
agentic laboratory dashboard. It shows how ingestion agents, analytics agents,
and an operations copilot can work together in one interface.

## What is included

- **Ingestion Agent (`agents/data_ingestion.py`)**
  - Normalizes records into a strict `LabResult` contract.
  - Supports built-in sample data, CSV, JSON, SQL/DB-API, and multi-source merge.

- **Analytics Agent (`agents/analytics.py`)**
  - Dashboard KPIs (test counts, pass/fail counts, pass rate, source count).
  - Pass rate by test type, daily volume trend, and threshold alerts.

- **Ops Copilot Agent (`agents/chat_agent.py`)**
  - Deterministic responses (no external LLM required).
  - Answers KPI summary, pass-rate questions, trend questions, failing sample lists.

- **Streamlit Command Center (`dashboard/app.py`)**
  - Multi-mode source connections.
  - KPI cards + alert panel.
  - Overview charts + records table + embedded copilot.

- **Demo Automation**
  - `demo_run.py` prints a deterministic report for quick validation.
  - `Makefile` shortcuts for install/test/demo/ui commands.
  - `Dockerfile` for containerized one-command launch.

## Quick start

```bash
python -m pip install -r requirements.txt
python demo_run.py
python -m streamlit run dashboard/app.py
```

## One-command options

```bash
make install
make test
make demo
make run-ui
```

## Docker demo

```bash
docker build -t lab-dashboard-demo .
docker run --rm -p 8501:8501 lab-dashboard-demo
```

Then open `http://localhost:8501`.

## Suggested live demo flow (5 minutes)

1. Run `python demo_run.py` to show deterministic KPI and copilot outputs.
2. Launch UI and review KPI cards + monitoring alerts.
3. In **Overview**, show pass-rate and daily trend charts.
4. In **Records**, show normalized schema fields.
5. In **Ops Copilot**, ask:
   - `Give KPI summary`
   - `pass rate by test`
   - `daily volume trend`
   - `list failed samples`
6. Switch source mode to CSV/JSON/SQLite to demonstrate connector flexibility.

## Data contract

Required fields:
- `sample_id`
- `test_name`
- `value`
- `passed`

Optional fields:
- `measured_at` (ISO datetime preferred)
- `source_system`
- `technician`

Missing timestamps default to current UTC for continuity.
