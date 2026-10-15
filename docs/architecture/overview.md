# Architecture overview

**Status:** Draft. This describes the *intended* design; none of these components exist yet.
**Owner:** R1 (Anthony), with all subsystem owners.

## 1. Purpose

EmberFlow is a distributed edge research prototype. Three Raspberry Pi 5 stations run smoke
inference locally on live or prerecorded video. A central FastAPI controller registers the
stations, collects telemetry and detections, tracks station health, and runs the one required
automated recovery action: **inference FPS reduction**. Operators review detections in a
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

This is a logical view, not a decision about physical network layout or cloud hosting.

## 3. Layers and responsibilities

| Layer | Runs on | Responsibilities | Owner | Repo path |
|---|---|---|---|---|
| Video input | Pi 5 / sim | Camera or prerecorded-file frames; adjustable processing FPS | R2 | `edge/video` |
| Inference | Pi 5 / sim | Primary + lightweight model; emits prediction, confidence, model version, latency | R3 (interface), R2 (integration) | `ml/inference` |
| Edge telemetry | Pi 5 / sim | CPU, memory, temperature, latency, FPS, network, camera, model version | R2 | `edge/telemetry` |
| Edge buffer | Pi 5 / sim | Durable store-and-forward; replay with stable IDs and source timestamps | R2 (+R4) | `edge/buffering` |
| Edge agent | Pi 5 / sim | Registration, messaging client, FPS command execution and reporting | R2 | `edge/agent` |
| Messaging | Central host | Transport for telemetry, detections, commands, results, acks | R4 | `controller/messaging` |
| Controller API | Central host | Registration, ingestion, health/stale checks, REST for dashboard | R4 | `controller/api` |
| Policy + recovery | Central host | FPS policy evaluation, command lifecycle, verification, audit | R4 | `controller/policies`, `controller/recovery` |
| Storage | Central host | Stations, detections, telemetry (TimescaleDB), commands/audit | R5 | `data/` |
| Dashboard | Operator browser | Station status, detections, confirm/dismiss, history | R5 | `dashboard/frontend` |
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
  -> controller ingestion -> DB commit -> durable ack to station
  -> dashboard (REST) -> operator confirm / dismiss
```

### 4.2 Network outage

- The Pi **keeps** reading video and running inference.
- Detection and telemetry records are written to the durable local buffer.
- The controller sees that the station has stopped reporting and marks its information
  **stale**. It does **not** assume the Pi has stopped processing.
- The dashboard shows the station as stale and when it last reported.

### 4.3 Reconnection and replay

- Buffered records replay with their **original `event_id` and `source_timestamp`**.
- The controller **stores durably before acknowledging**. The station removes a record from
  the buffer only after it receives an ack with `stored` or `duplicate`.
- Duplicates are dropped by `event_id` (unique constraint) and acknowledged as `duplicate`.
- Delayed telemetry is stored as history but **must not overwrite newer station state**.
  "Current state" comes from the newest `source_timestamp` (or `sequence`), not arrival order.
- FPS commands that expired while the station was offline are **never applied**. The station
  reports `failed` with an expiry reason.

### 4.4 FPS adaptation (required recovery action)

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

## 5. Cross-cutting concerns

- **Identity:** each station has a stable `station_id` set in its config.
- **Time:** all timestamps are UTC RFC 3339. Pis should run NTP. Clock skew between Pis and the
  central host is a known risk; the controller stores both `source_timestamp` and its own
  `received_at`.
- **Idempotency:** `event_id` (UUID) is assigned once at the source and never regenerated.
- **Versioning:** each message carries `schema_version`; breaking changes bump it.
- **Security (prototype level):** no secrets in Git, configuration via `.env`. Broker and API
  authentication depend on the messaging decision and are still to be designed.

## 6. Open architectural decisions

| Decision | State | Owner(s) | Impact on this document |
|---|---|---|---|
| Messaging: MQTT vs NATS | OPEN | Gabe | Transport, QoS/ack semantics, reconnection behaviour |
| Edge buffer implementation | SQLite suggested | Tomiwa with Gabe | Persistence and ack/delete rules |
| Offline alert snapshots | OPEN | Tomiwa, Gabe, Ethan | Whether review imagery is captured/buffered offline (`snapshot_ref`) |
| ML baseline and dataset | OPEN | Diego | Model versions, latency budget, inference interface details |
| FPS thresholds and evaluation | OPEN | Gabe, Tomiwa, Dylan | Policy configuration values |
| Redis | Not required | Ethan | Add only if a measured performance need arises |
| OD-1 … OD-7 | To reconcile | — | Official Jira IDs/owners/dates still to be matched; meanings not restated here |

See [decisions/README.md](../decisions/README.md).
