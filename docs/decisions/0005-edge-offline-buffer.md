# 0005: Edge offline buffer implementation

- **Status:** **Proposed** (SQLite recommended, not formally finalized)
- **Date:** _TBD_
- **Owner:** R2 (Tomiwa) with R4 (Gabe)
- **Reviewers:** R1 (Anthony), R6 (Dylan)

## Context

During connectivity loss, inference continues and detection/telemetry records must be kept
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
- Ack rule: delete or mark a record only after a controller `ack` with `stored` or `duplicate`.
- Size limits and what happens when storage is full (which records are dropped first).
- Whether offline alert snapshots/images are buffered (separate OPEN decision).
- SD-card wear and durability settings (e.g. WAL mode).

## Verification

Fault-injection test: disconnect → keep generating records → reconnect, then check that every
record arrives exactly once in the database with its original timestamps.
