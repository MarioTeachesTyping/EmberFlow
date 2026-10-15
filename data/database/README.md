# Database schema

**Owner:** R5 — Ethan  
**Status:** Not implemented — scaffold only.

PostgreSQL + TimescaleDB design (ADR 0002).

## Planned contents

- `stations`, `detections`, `telemetry` (hypertable), `commands` / audit tables
- Unique constraint on `event_id` to make replay idempotent
- Separate `source_timestamp` and `received_at` columns

## Boundaries

Delayed telemetry must not overwrite newer station state.
