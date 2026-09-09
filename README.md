# Agentic Shadow for Autonomous Infrastructure Operations

A functioning multi-agent digital twin that turns simulated infrastructure telemetry into explainable, policy-gated, auditable remediation workflows.

> **Safety scope:** every action changes simulated state only. No component connects to or controls physical equipment, and medium-or-higher-risk actions require a human decision.

## Overview
Agentic Shadow ingests typed telemetry, persists it, evaluates configurable rules, creates incidents, coordinates deterministic specialist agents, enforces action policy, and records the whole lifecycle. It works offline without an LLM key; PostgreSQL is the intended runtime datastore and SQLite is the zero-infrastructure default.

## Why This Project Exists
The project demonstrates practical backend and agent architecture without disguising rules as machine learning or allowing probabilistic output to bypass operational safety.

## System Architecture
```
Simulator -> FastAPI -> SQLAlchemy/PostgreSQL -> Rule Detector -> Incident
                                                               |
                                                        Supervisor Agent
                                                      /                  \
                                            Diagnostic Agent      Remediation Agent
                                                      \                  /
                                                       Policy Engine
                                                      /             \
                                               low-risk auto      human approval
                                                      \             /
                                               Simulated Execution -> Audit/Rollback
```

## Agent Workflow
The provider-neutral `BaseAgent` contract supports structured inputs and outputs. The local `SupervisorAgent` invokes deterministic diagnostic and remediation agents. `AGENT_PROVIDER=local` is the only implemented provider; a Google ADK adapter is deliberately deferred until its model/session/tool lifecycle can be integrated and tested against the real SDK rather than invented.

## Safety Model
Proposals carry explicit `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` risk. Only low-risk simulation actions auto-execute. All others enter `AWAITING_APPROVAL`; approval/rejection is attributed in the audit log. See [the safety model](docs/safety-model.md).

## Tech Stack
Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2, PostgreSQL 16/SQLite, pytest, and Docker Compose.

## Repository Structure
`app/api` exposes transport concerns; `agents`, `detection`, and `safety` hold domain decisions; `services` orchestrates use cases; `database` provides persistence; `simulator` generates inputs; `tests` validates behavior; and `docs` records design decisions.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
make install
cp .env.example .env       # optional; default is local SQLite
make test
make run
```
Open `http://127.0.0.1:8000/docs` for interactive OpenAPI documentation.

## Running PostgreSQL
```bash
make db-up
# Set DATABASE_URL to postgresql+psycopg://agentic_shadow:local-development-only@localhost:5432/agentic_shadow
```
The Compose credential is explicitly local-only; use secret management outside development.

## Starting the API
`make run` starts Uvicorn with reload. Tables are created on startup for this MVP; migrations are a roadmap item.

## Running the Simulator
`make simulator` prints healthy transformer JSON. Inject an anomaly with:
```bash
python -m simulator.telemetry_generator --asset-type transformer --anomaly overheating
```

## Running the Demo
`make demo` runs healthy ingestion, anomalous ingestion, agent investigation, policy review, human approval, simulated execution, and audit output entirely locally.

## Running Tests
`make test` uses deterministic generated data and an isolated SQLite database; Docker is not required.

## API Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Readiness response |
| POST | `/telemetry` | Validate, persist, and evaluate telemetry |
| GET | `/telemetry/recent` | Recent readings (`limit` 1–500) |
| GET | `/incidents` | Incident list |
| GET | `/incidents/{id}` | Investigation, evidence, and actions |
| POST | `/incidents/{id}/approve` | Attribute approval and execute pending simulations |
| POST | `/incidents/{id}/reject` | Attribute rejection |
| GET | `/audit` | Reverse-chronological audit events |

## Example Incident Lifecycle
A 125°C transformer reading violates its 95°C limit and becomes `CRITICAL`. The diagnostic agent identifies likely thermal-management failure. Monitoring auto-executes because it is low risk; simulated shutdown waits for a named human actor, then executes or is rejected. Every transition is durable.

## Roadmap
- A tested Google ADK provider adapter and durable agent sessions
- Alembic migrations, authentication/RBAC, pagination, and observability
- Event broker/background workers and streaming telemetry
- Baseline-aware statistical/ML detector behind the existing boundary
- Action-specific rollback API and chaos/failure simulation
