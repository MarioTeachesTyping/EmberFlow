# Edge offline buffer

**Owner:** R2 — Tomiwa (with R4 — Gabe)  
**Status:** Not implemented — scaffold only.

Durable local store for detection and telemetry records during connectivity loss, replayed on reconnection with stable event IDs and original source timestamps.

## Planned contents

- Persistence layer (SQLite recommended — ADR 0005, not finalized)
- Replay loop that deletes/marks records only after a durable controller acknowledgment
- Policy for expired FPS commands on reconnect (never apply them)

## Boundaries

Whether alert snapshots/images are buffered offline is OPEN (decision register).
