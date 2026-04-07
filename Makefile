.PHONY: install test demo run-ui

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

demo:
	python demo_run.py

run-ui:
	python -m streamlit run dashboard/app.py
