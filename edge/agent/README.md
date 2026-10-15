# Edge agent

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Long-running station process that wires video, inference, telemetry and buffering together, registers with the controller, and receives/acknowledges FPS commands.

## Planned contents

- Station registration using the envelope in `docs/api/contracts.md`
- Messaging client behind an interface (MQTT vs NATS is OPEN — ADR 0004)
- FPS command handler: reject expired commands, apply, report `accepted`/`applied`/`failed`
- A simulated-station mode so every developer can run without a Pi

## Boundaries

Must keep processing locally when the controller is unreachable.
