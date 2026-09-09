# Safety Model

Agentic Shadow is a decision-support simulation, not an industrial control system. An AI agent must not directly control critical infrastructure: model output can be incorrect, ambiguous, prompt-influenced, or produced without full physical context.

## Permission boundaries

Agents may inspect incident evidence and propose typed actions. They cannot approve or execute them. The deterministic policy engine is the authority that routes actions, and the executor can mutate only digital-twin state. Real device protocols and credentials are intentionally absent.

## Risk and approval

| Risk | Examples | Gate |
|---|---|---|
| LOW | collect telemetry, increase monitoring, restart simulated sensor | automatic |
| MEDIUM | restart simulated noncritical service | human |
| HIGH | simulated shutdown or operating-limit change | human |
| CRITICAL | safety-critical impact | human; future multi-party gate |

A proposal at medium risk or above places its incident in `AWAITING_APPROVAL`. A named actor must approve or reject it through the API. A recommendation never serves as authorization.

## Simulated execution and rollback

Execution records pre-action state, applies an explicit simulated post-state, and emits an audit event. The executor also implements restoration from the pre-state and records `ROLLBACK_EXECUTED`; exposing action-specific rollback authorization is intentionally a next-phase API feature.

## Auditability

Structured, timestamped records attribute lifecycle events and human decisions. This enables reconstruction without depending on agent prose. Production hardening should add immutable external log export, authenticated identities, retention controls, and cryptographic integrity.
