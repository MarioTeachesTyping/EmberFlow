# Controller messaging

**Owner:** R4 — Gabe  
**Status:** Not implemented — scaffold only.

Broker-facing ingestion of telemetry/detection/command-result messages and publication of FPS commands and durable acknowledgments.

## Planned contents

- Transport adapter behind an interface so MQTT or NATS can be selected by config
- Store-then-acknowledge ingestion with deduplication by `event_id`

## Boundaries

MQTT vs NATS is OPEN (ADR 0004). Do not hard-code one.
