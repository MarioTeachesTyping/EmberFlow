# Edge (Raspberry Pi 5 stations)

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Everything that runs on each of the three Raspberry Pi 5 stations, or on a simulated station on a developer laptop.

## Planned contents

- `agent/` — station process: registration, messaging client, command handling
- `telemetry/` — CPU, memory, temperature, latency, FPS, network/camera status, active model version
- `video/` — live camera or prerecorded-video input pipeline
- `buffering/` — durable offline buffer and replay (SQLite recommended, not final)

## Boundaries

Does not own ML training (R3) or central FPS policy selection (R4). Executes FPS commands; does not decide them.
