# Edge agent

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Long-running station process that wires video, inference, telemetry and buffering together, registers with the controller, and receives/acknowledges FPS commands.

## Planned contents

- Station registration through an interface to be frozen with R1/R4 (registration is not a v0 message type)
- Messaging client behind an interface (MQTT vs NATS is OPEN — ADR 0004)
- Command handlers: validate schema, target, bounds, expiry and duplicate ID; report correlated outcomes
- FPS/resolution/model changes, known-good rollback and designated processing workers; wire formats remain to be reviewed
- A simulated-station mode so every developer can run without a Pi

## Boundaries

Must keep processing locally when the controller is unreachable and its local input remains available. Provide versioned setup/configuration and a deterministic adapter fixture so a teammate can integrate algorithms before final model availability.
