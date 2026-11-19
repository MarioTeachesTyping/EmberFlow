# 0004: Messaging transport: MQTT with Mosquitto

- **Status:** Accepted
- **Date:** 2026-11-19
- **Owner:** R4 (James)
- **Reviewers:** R2 (Tomiwa), R1 (Anthony), R6 (Dylan)

## Context

Stations publish telemetry, detections and command results. The controller sends commands
and durable acknowledgments. Connectivity can drop, and replayed records must not be accepted
twice. The broker runs on the team-owned central computer.

## Options considered

| Option | Notes |
|---|---|
| **MQTT with Eclipse Mosquitto** | Selected |
| NATS (with JetStream) | Not selected |

The comparison table this ADR originally called for (delivery guarantees, reconnection,
duplicates, setup effort, Python clients, Pi 5 resource use) was not filled in from
prototypes before the decision. The decision was made by the messaging owner; the
disconnect/reconnect prototype below still has to be run.

## Decision

Use **MQTT** as the edge/controller messaging protocol, with **Eclipse Mosquitto** as the
broker on the central host. Confirmed by R4 James Connolly (backend owner); recorded by R1
Anthony Terry on November 19, 2026.

This closes the transport part of SRS OD 2. These parts of OD 2 remain open and still need
owner decisions and contract updates:

- MQTT protocol version (3.1.1 or 5), Mosquitto version and Python client library
- Topic names, QoS levels, retained messages and persistent-session settings
- Broker authentication, access control and TLS on the team LAN
- The image transfer path and complete durable-receipt semantics (SRS SI-1.7)

## Consequences

- `controller/messaging` and `edge/agent` use an MQTT client. Keeping it behind a small
  interface is still useful for tests and fault injection, but no NATS adapter is planned.
- `.env.example` drops `MESSAGING_BACKEND` and `NATS_URL`; `MQTT_URL` points at Mosquitto.
- End-to-end reliability still comes from `event_id` deduplication and store-then-ack at the
  controller, not from MQTT QoS. A broker delivery acknowledgment is not completion receipt.
- The message contract ([docs/api/contracts.md](../api/contracts.md)) keeps its JSON body;
  topic names and QoS are added to it once agreed.

## Verification

A disconnect/reconnect prototype against Mosquitto that measures duplicate and lost-message
counts, run before the integration contract freeze.
