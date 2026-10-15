# Adaptation policies

**Owner:** R4 — Gabe  
**Status:** Not implemented — scaffold only.

Evaluates resource telemetry over a stable observation window and decides when to issue an FPS reduction command.

## Planned contents

- Configurable triggers: sustained temperature, sustained latency, or another approved condition
- Cooldown/hysteresis to prevent oscillation

## Boundaries

Thresholds are OPEN and must be benchmarked on the Pi 5. Example values in docs are illustrative only.
