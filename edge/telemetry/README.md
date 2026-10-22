# Edge telemetry

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Collects station health metrics and emits `telemetry` messages.

## Planned contents

- CPU %, memory %, SoC temperature, inference latency, processing FPS
- Network status, camera status, active model version, free storage and evidence backlog
- Defined units, station/session/sequence identity, source time and clock validity; historical replay must not reset liveness

## Boundaries

The legacy v0 schema covers only part of v1.1. Agree missing fields with R1/R4 and version schemas/fixtures together before integration; do not treat v0 fixture success as full telemetry acceptance.
