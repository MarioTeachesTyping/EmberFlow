# Architecture overview

**Status:** Draft. This describes the *intended* design; none of these components exist yet.
**Owner:** R1 (Anthony), with all subsystem owners.

## 1. Purpose

EmberFlow is a distributed edge research prototype. Three Raspberry Pi 5 stations run smoke
inference locally on live or prerecorded video. A central FastAPI controller registers the
stations, collects telemetry and complete detection/image evidence, tracks health and trust,
and coordinates FPS/resolution/model adaptation, workload movement and model lifecycle.
FPS reduction is the first policy slice. Operators review detections in a
React + TypeScript dashboard. Data is stored in PostgreSQL + TimescaleDB.

The research contribution is the **integration**: local inference, health monitoring, offline
continuity, human review and measured recovery. It is not a new detector.

## 2. Logical architecture

```
[Operator: React + TypeScript dashboard]
              | REST API
              v
[Central Controller: FastAPI] <----> [PostgreSQL + TimescaleDB]
 - station registration               - stations
 - telemetry / event ingestion        - detections
 - health + stale-state checks        - telemetry (hypertable)
 - FPS adaptation policy              - commands / audit
 - durable acknowledgments
              |
     MQTT or NATS (OPEN — ADR 0004)
   telemetry, detections, commands, acks
              |
   +----------+----------+
   |          |          |
[Pi 5 #1]  [Pi 5 #2]  [Pi 5 #3]
video+ML   video+ML   video+ML
telemetry  telemetry  telemetry
buffer     buffer     buffer
FPS ctl    FPS ctl    FPS ctl
```

This is a logical view. The October 22 physical baseline uses an existing central computer,
wired Ethernet through a switch/router, and one USB webcam to be tested on all three Pis.
Replay supplies the other two inputs. The demonstration is indoors with mains power and no
custom PCB. See [deployment](deployment.md) and
[ADR 0007](../decisions/0007-october-22-review-baseline.md); full-team approval is pending.

## 3. Layers and responsibilities

| Layer | Runs on | Responsibilities | Owner | Repo path |
|---|---|---|---|---|
| Video input | Pi 5 / sim | Camera or prerecorded-file frames; adjustable processing FPS | R2 | `edge/video` |
| Inference | Pi 5 / sim | Primary + lightweight model; emits prediction, confidence, model version, latency | R3 (interface), R2 (integration) | `ml/inference` |
| Edge telemetry | Pi 5 / sim | CPU, memory, temperature, latency, FPS, network, camera, model version | R2 | `edge/telemetry` |
| Edge buffer | Pi 5 / sim | Durable metadata/image evidence and retained telemetry; bounded replay with stable identity/time | R2 (+R4) | `edge/buffering` |
| Edge agent | Pi 5 / sim | Registration, messaging client, FPS command execution and reporting | R2 | `edge/agent` |
| Messaging | Central host | Transport for telemetry, detections, commands, results, acks | R4 | `controller/messaging` |
| Controller API | Central host | Registration, ingestion, health/stale checks, REST for dashboard | R4 | `controller/api` |
| Policy + recovery | Central host | Resource/trust policies, command verification, candidate rollout/rollback, workload coordination, audit | R4 | `controller/policies`, `controller/recovery` |
| Storage | Central host | Stations, complete detections/images, telemetry, deployments/comparisons, review and audit | R5 | `data/` |
| Dashboard | Operator browser | Health/trust, image review, configurable limits, model approval/deployment and audit | R5 | `dashboard/frontend` |
| Testing & experiments | Dev / CI / lab | Tests, fault injection, reliability metrics | R6 | `testing/`, `experiments/` |

**Design principle:** use practical modules inside **one** FastAPI app and **one** edge agent
rather than many separately deployed microservices.

## 4. Primary data flows

### 4.1 Normal operation

```
camera / prerecorded video
  -> edge video pipeline
  -> ML inference (on the Pi)
  -> detection + telemetry messages (envelope with event_id, source_timestamp)
  -> messaging transport
  -> controller + persistence: metadata AND representative image durable/retrievable
  -> complete evidence receipt to station (format pending)
  -> dashboard (REST) -> operator confirm / dismiss
```

### 4.2 Network outage

- The Pi **keeps** reading video and running inference.
- Accepted metadata plus one recoverable image per event, and retained telemetry, are written to a bounded durable outbox. Record accepted/rejected evidence and storage failures; do not promise unlimited retention.
- The controller sees that the station has stopped reporting and marks its information
  **stale**. It does **not** assume the Pi has stopped processing.
- The dashboard shows the station as stale and when it last reported.

### 4.3 Reconnection and replay

- Buffered records replay with their **original `event_id` and `source_timestamp`**.
- Metadata and image may arrive separately; expose incomplete state until both are durable,
  integrity-checked under the agreed policy, and jointly reviewable. Only a complete durable
  receipt permits post-receipt local cleanup. Legacy v0 metadata acks are insufficient.
- Retransmission is allowed after a lost receipt; deduplicate logically by stable event identity
  and never confuse existing metadata with a complete image. Test partial upload and restart.
- Delayed telemetry stays in history and must not overwrite newer measurements. Source time,
  session/sequence and clock validity guide ordering; current liveness needs fresh contact under
  the agreed timeout rules. Neither replay arrival nor an unchecked source timestamp proves health.
- FPS commands that expired while the station was offline are **never applied**. The station
  reports `failed` with an expiry reason.

### 4.4 FPS adaptation (first required recovery slice)

```
Pi reports resource telemetry
  -> controller evaluates configurable policy over a stable observation window
     (not on a single noisy sample) and records baseline telemetry
  -> controller creates FPS command (unique command_id, station_id, requested_fps,
     created_at, expires_at, policy_reason)                        state: requested
  -> Pi receives, checks expiry, accepts                            state: accepted
  -> Pi changes processing FPS and reports actual applied FPS      state: applied
  -> later telemetry compared with baseline by controller          state: verified | failed
  -> cooldown / hysteresis window prevents oscillation
```

An acknowledgment alone is **not** proof of recovery. Only `verified` means the measured FPS
changed and the resource condition improved compared with the baseline.

Lifecycle states (proposal; see [contracts](../api/contracts.md#4-fps-command-lifecycle)):

| State | Set by | Meaning |
|---|---|---|
| `requested` | Controller | Command created and sent; baseline recorded |
| `accepted` | Station | Station received an unexpired command |
| `applied` | Station | Station changed its processing FPS; reports actual FPS |
| `verified` | Controller | Later telemetry confirms the FPS change and an improvement vs. baseline |
| `failed` | Either | Rejected, expired, not applied, or no measured improvement (with reason) |

Trigger thresholds, observation windows, target FPS, cooldown and success criteria are
**not decided**. They must be measured on the chosen Pi 5 configuration. Any numbers in
examples (such as 10 → 5 FPS) are illustrative only.

### 4.5 Trust, model lifecycle and workload movement

Diego supplies the image-quality/input-change/disagreement methods and versioned models;
Tomiwa integrates them on the shared platform. James coordinates policy, candidate/shadow
comparison, limited rollout, model changes and known-good rollback. Ethan exposes comparison,
human feedback, configuration/deployment controls and audit records. A candidate does not
control active alerts during shadow evaluation. Numerical methods/thresholds remain open.

Resolution/model control and workload movement remain required alongside FPS control. A moved
worker must have a source accessible on its destination; a USB webcam does not move across
Ethernet by itself. Define that scenario before the migration test. Every action needs a
correlated outcome and reproducible before/action/after evidence, not merely a command ack.

## 5. Cross-cutting concerns

- **Identity:** each station has a stable `station_id` set in its config.
- **Time:** all timestamps are UTC RFC 3339. Pis should run NTP. Clock skew between Pis and the
  central host is a known risk; store source and receive time, session/sequence and clock validity. Use fresh heartbeat/contact rules for liveness and monotonic durations for latency; neither arrival order nor source time alone proves current health.
- **Idempotency:** `event_id` (UUID) is assigned once at the source and never regenerated.
- **Versioning:** each message carries `schema_version`; breaking changes bump it.
- **Security (prototype level):** no secrets in Git, configuration via `.env`. Broker and API
  authentication depend on the messaging decision and are still to be designed.

## 6. Open architectural decisions

Use the [decision register](../decisions/README.md) for all ten SRS open items and closure gates.
Physical Ethernet, USB camera type and required image retention are in the review baseline;
exact parts, transport/receipt, algorithms, profiles, capacity, budget and host configuration
remain open. The [legacy contract gaps](../api/contracts.md#7-gaps-before-v11-integration) must
be closed before treating Proposal v0 as an integration contract.
