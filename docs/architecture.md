# Architecture

## Processing pipeline

1. **Telemetry** — the simulator or caller submits a validated, timestamped equipment reading through FastAPI.
2. **Detection** — `RuleBasedAnomalyDetector` selects per-asset thresholds and returns structured anomalies and severity. Its narrow `detect` boundary permits a future statistical implementation.
3. **Incident** — the service persists affected asset, evidence, anomaly descriptions, severity, and state.
4. **Supervisor Agent** — coordinates investigation and retains provider independence.
5. **Diagnostic Agent** — produces probable cause, bounded confidence, and supporting evidence as a typed `Diagnosis`.
6. **Remediation Agent** — returns typed action proposals with risk, rationale, and parameters.
7. **Policy Engine** — evaluates every proposal; agent recommendations never grant their own permission.
8. **Approval** — low risk is automatically approved; medium, high, and critical proposals wait for an attributed human API decision.
9. **Execution** — `SimulatedActionExecutor` snapshots pre-state and records post-state. It has no physical control integration.
10. **Audit** — append-style events capture telemetry, detection, investigation, policy, decisions, execution, and rollback.

## Persistence and transaction boundary

SQLAlchemy maps the domain to PostgreSQL in normal deployment and SQLite in local/test use. Telemetry and its resulting workflow commit together. Relationships preserve incident/action state, while JSON columns retain structured evidence and metadata. Automatic table creation keeps the MVP immediately runnable; Alembic migrations are planned before production use.

## Agent provider boundary

`BaseAgent[Input, Output]` defines the replaceable execution boundary. Local agents are deterministic and require no credentials. A future ADK implementation should translate these Pydantic contracts to real ADK tools/sessions behind this boundary; provider selection must fail closed and retain policy enforcement outside the model.
