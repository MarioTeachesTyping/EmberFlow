# Central controller (FastAPI)

**Owner:** R4 — Gabe  
**Status:** Not implemented — scaffold only.

Single FastAPI application that coordinates the stations. Prefer modules inside this one app over separate microservices.

## Planned contents

- `api/` — REST endpoints for the dashboard and station registration
- `messaging/` — broker client and ingestion (MQTT vs NATS OPEN)
- `policies/` — FPS adaptation policy evaluation
- `recovery/` — FPS command lifecycle, verification, replay acknowledgment

## Boundaries

Works with R2 on the edge protocol. The database schema is owned by R5. The controller does not run per-frame inference.
