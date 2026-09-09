.PHONY: install test run demo simulator db-up db-down
install:
	python -m pip install -e ".[dev]"
test:
	python -m pytest
run:
	uvicorn app.main:app --reload
demo:
	python scripts/demo.py
simulator:
	python -m simulator.telemetry_generator
db-up:
	docker compose up -d
db-down:
	docker compose down
