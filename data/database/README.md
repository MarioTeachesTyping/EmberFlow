# Database schema

**Owner:** R5 — Ethan  
**Status:** Not implemented — scaffold only.

PostgreSQL + TimescaleDB design (ADR 0002).

## Planned contents

- Stations/hardware config, detections/images, telemetry, deployments/candidate comparisons, reviews, commands and audit records
- Image ID/event association, encoding, byte count, integrity and incomplete/complete synchronization state
- Unique constraint on `event_id` to make replay idempotent
- Separate `source_timestamp` and `received_at` columns

## Boundaries

Delayed telemetry must not overwrite newer station state. Image metadata does not itself provide durable image storage; jointly reviewable image persistence, retention and completion must be designed with R4/R2. Keep station/session/sequence and source/receive times distinct.
