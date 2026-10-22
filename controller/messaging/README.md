# Controller messaging

**Owner:** R4 — James Connolly

**Status:** Not implemented — scaffold only.

Broker-facing ingestion of telemetry/detection/command-result messages and publication of FPS commands and durable acknowledgments.

## Planned contents

- Transport adapter behind an interface so MQTT or NATS can be selected by config
- Store-then-acknowledge ingestion with deduplication by `event_id`
- Detection completion only after metadata and image are durable and jointly retrievable; metadata-only receipt is not completion
- Session/sequence freshness rules separate replay history from current station state

## Boundaries

MQTT vs NATS is OPEN (ADR 0004). Do not hard-code one.
