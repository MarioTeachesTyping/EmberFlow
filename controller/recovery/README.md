# Recovery / command lifecycle

**Owner:** R4 — Gabe  
**Status:** Not implemented — scaffold only.

Tracks each FPS command through requested → accepted → applied → verified | failed and records audit evidence.

## Planned contents

- Baseline telemetry capture before the command
- Verification by comparing post-command telemetry to the baseline
- Expiry handling so stale commands are never applied on reconnect

## Boundaries

An acknowledgment alone is not proof of recovery. Rollback, canary and workload migration are stretch goals.
