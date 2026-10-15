# Edge telemetry

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Collects station health metrics and emits `telemetry` messages.

## Planned contents

- CPU %, memory %, SoC temperature, inference latency, processing FPS
- Network status, camera status, active model version

## Boundaries

Field names must match `docs/api/schemas/edge-messages.v0.schema.json`.
