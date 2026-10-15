# 0002: Central database: PostgreSQL with TimescaleDB

- **Status:** Accepted
- **Date:** 2026-10-14 (recorded from the architecture handoff)
- **Owner:** R5 (Ethan)
- **Reviewers:** R4 (Gabe), R1 (Anthony)

## Context

The controller stores station metadata, detections, operator reviews, FPS command audit
records, and high-volume time-series telemetry. Records can arrive late (offline replay), so
storage must keep source timestamps and deduplicate.

## Decision

Use **PostgreSQL with the TimescaleDB extension**, running on the team-owned central computer.
Telemetry goes in a TimescaleDB hypertable. Relational data (stations, detections, commands,
audit) goes in regular tables.

## Consequences

- `event_id` gets a unique constraint so replay is idempotent.
- Tables store both `source_timestamp` and `received_at`.
- Current station state comes from the newest source time, not from arrival order.
- A migration tool still needs to be chosen (open).
- Redis is **not** part of the baseline. Add it only if a measured need appears.

## Verification

Migration applies cleanly; replay/dedup integration test; telemetry query performance checked
for dashboard history views.
