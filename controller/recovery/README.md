# Recovery / command lifecycle

**Owner:** R4 — James Connolly

**Status:** Not implemented — scaffold only.

Tracks each FPS command through requested → accepted → applied → verified | failed and records audit evidence.

## Planned contents

- Baseline telemetry capture before the command
- Verification by comparing post-command telemetry to the baseline
- Expiry handling so stale commands are never applied on reconnect

## Boundaries

An acknowledgment alone is not proof of recovery. Candidate/shadow evaluation, limited rollout, known-good rollback and workload movement remain required in v1.1. Wire formats and policies are not implemented. A USB camera remains attached to its Pi; a workload move needs an input accessible at the destination. Shared recorded footage is a recommended scenario, not an approved live-camera failover design.
