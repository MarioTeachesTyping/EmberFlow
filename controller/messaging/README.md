# Controller messaging

**Owner:** R4 — James Connolly

**Status:** Not implemented — scaffold only.

Broker-facing ingestion of telemetry/detection/command-result messages and publication of FPS commands and durable acknowledgments.

## Planned contents

- MQTT client for the Mosquitto broker, behind a small interface so tests can substitute a fake
- Store-then-acknowledge ingestion with deduplication by `event_id`
- Detection completion only after metadata and image are durable and jointly retrievable; metadata-only receipt is not completion
- Session/sequence freshness rules separate replay history from current station state

## Boundaries

MQTT with Mosquitto is accepted ([ADR 0004](../../docs/decisions/0004-messaging.md)). MQTT
version, client library, topics, QoS and broker access are still open; do not hard-code
guesses. A broker delivery acknowledgment is not completion receipt.
