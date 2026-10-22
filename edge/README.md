# Edge (Raspberry Pi 5 stations)

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Everything that runs on each of the three Raspberry Pi 5 stations, or on a simulated station on a developer laptop.

## Planned contents

- `agent/` — station process: registration, messaging client, command handling
- `telemetry/` — CPU, memory, temperature, latency, FPS, network/camera status, active model version
- `video/` — live camera or prerecorded-video input pipeline
- `buffering/` — durable metadata/image outbox, retained telemetry, bounded retention and safe replay (SQLite proposed)
- Common hardware/software configuration, power/cooling/storage/network evidence and teammate setup/model-adapter handoff

## Boundaries

R3 owns algorithms/models; R4 owns central policy. R2 integrates the algorithms and executes valid FPS/resolution/model/worker commands, retaining a known-good model for rollback. No custom PCB is required. See the [edge specification](../docs/specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.md).
