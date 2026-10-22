# Edge offline buffer

**Owner:** R2 — Tomiwa Aluko (with R4 — James Connolly)

**Status:** Not implemented — scaffold only.

Durable local store for accepted detection metadata plus one representative image per event, and retained telemetry. Replay preserves event/station/session/frame identity and original source time.

## Planned contents

- Persistence layer (SQLite recommended — ADR 0005, not finalized)
- Replay loop retaining pending metadata/images until central receipt confirms both are durable and reviewable
- Restart recovery, partial-image retry, integrity checks, quotas/reserve, backlog and explicit admission/retention failures
- Policy for expired FPS commands on reconnect (never apply them)

## Boundaries

Representative images are required by the v1.1 review baseline. Image transfer, integrity, capacity limits, retention and receipt format remain open; legacy v0 metadata-only acknowledgments cannot authorize image cleanup. See [contracts](../../docs/api/contracts.md#7-gaps-before-v11-integration).
