# 0004: Messaging transport: MQTT vs NATS

- **Status:** **OPEN** (not decided)
- **Date:** _TBD_
- **Owner:** R4 (James)
- **Reviewers:** R2 (Tomiwa), R1 (Anthony), R6 (Dylan)

## Context

Stations publish telemetry, detections and command results. The controller sends FPS commands
and durable acknowledgments. Connectivity can drop, and replayed records must not be accepted
twice. The broker runs on the team-owned central computer.

## Options considered

| Criterion | MQTT (e.g. Mosquitto) | NATS (e.g. NATS + JetStream) |
|---|---|---|
| Reliability / delivery guarantees | _to evaluate_ | _to evaluate_ |
| Reconnection behaviour | _to evaluate_ | _to evaluate_ |
| Duplicate handling | _to evaluate_ | _to evaluate_ |
| Setup / operational effort | _to evaluate_ | _to evaluate_ |
| Python client maturity (edge + FastAPI) | _to evaluate_ | _to evaluate_ |
| Resource use on Pi 5 | _to evaluate_ | _to evaluate_ |

Fill in this table from hands-on prototypes, not from assumptions.

## Decision

_None yet._ Until this is accepted:

- Code must go through a transport interface (`controller/messaging`, `edge/agent`).
- `MESSAGING_BACKEND` in `.env.example` stays empty.
- The message contract ([docs/api/contracts.md](../api/contracts.md)) stays transport-agnostic.
  End-to-end reliability comes from `event_id` dedup and store-then-ack, whichever broker is
  chosen.

## Verification

A disconnect/reconnect prototype with each candidate that measures duplicate and lost-message
counts.
