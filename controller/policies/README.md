# Adaptation policies

**Owner:** R4 — James Connolly

**Status:** Not implemented — scaffold only.

Evaluates resource and image/model trust signals and coordinates documented adaptation. FPS reduction is the first policy slice, not the only required recovery capability.

## Planned contents

- Configurable triggers: sustained temperature, sustained latency, or another approved condition
- Cooldown/hysteresis to prevent oscillation
- Resolution/model changes and workload movement using a source accessible to the receiving node
- Limits/methods and outcome criteria frozen with R2/R3/R6 before acceptance

## Boundaries

Thresholds are OPEN and must be benchmarked on the Pi 5. Example values in docs are illustrative only.
