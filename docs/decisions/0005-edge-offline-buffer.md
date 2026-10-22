# 0005: Edge offline buffer implementation

- **Status:** **Proposed** (SQLite recommended, not formally finalized)
- **Date:** _TBD_
- **Owner:** R2 (Tomiwa) with R4 (James)
- **Reviewers:** R1 (Anthony), R6 (Dylan)

## Context

During connectivity loss, inference continues and accepted detection metadata/images plus retained telemetry must be kept
**durably** on the Pi. They are replayed on reconnection with stable `event_id`s and original
`source_timestamp`s, and are never accepted twice.

## Options considered

| Option | Notes |
|---|---|
| **SQLite (recommended)** | Durable, transactional, in the Python standard library, single file |
| Append-only file / JSON lines | Simple, but harder to mark acks and survive partial writes |
| Broker-side persistence only | Depends on the open ADR 0004; doesn't cover controller-side store-then-ack |

## Decision

_Not finalized._ Still to define:

- Write path: every record goes through the buffer (outbox pattern) vs. only while offline.
- Completion rule: retain pending detection metadata/image association until a receipt covers both durable metadata and complete, reviewable image. Define the receipt and post-completion retention with R4/R5; v0 `stored`/`duplicate` metadata acknowledgments are insufficient.
- Size limits and what happens when storage is full (which records are dropped first).
- One representative image per accepted event is required by v1.1; format, integrity, upload, quotas/reserve, outage envelope and lifecycle are still open. See ADR 0007.
- SD-card wear and durability settings (e.g. WAL mode).

## Verification

Fault-injection test: disconnect → keep generating records → reconnect, then check that every
accepted event and image becomes reviewable once logically, with its original identity/time. Inject lost receipts, partial uploads, restart and capacity exhaustion; account for accepted/rejected evidence within a declared envelope.
