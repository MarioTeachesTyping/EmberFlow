# Interface contracts

> **PROPOSAL v0. Not yet approved.** This defines the *planned* edge event envelope, message
> payloads, FPS command lifecycle, durable acknowledgment and REST endpoints. Nothing here is
> implemented. Changes require the reviewers listed in
> [CONTRIBUTING.md § Cross-subsystem changes](../../CONTRIBUTING.md#cross-subsystem-changes).

- **Machine-readable schema:** [`schemas/edge-messages.v0.schema.json`](schemas/edge-messages.v0.schema.json) (JSON Schema 2020-12)
- **Example messages:** `testing/fixtures/contracts/valid/` and `.../invalid/`, checked by
  `testing/unit/test_edge_message_schema.py`
- **Owner:** R1 (coordination), R2 (edge side), R4 (controller side)

## 1. Transport independence

The messaging transport (**MQTT vs NATS**) is **OPEN** ([ADR 0004](../decisions/0004-messaging.md)).
The contract below is a JSON message body and works with either transport. Topic/subject
names, QoS levels and broker-level delivery guarantees will be defined once the ADR is
accepted. **Reliability must not depend on broker-level exactly-once delivery.** It comes from
stable `event_id`s, store-then-ack on the controller, and deduplication.

Topic/subject naming (placeholder, decided with ADR 0004):

| Direction | Message types | Placeholder name |
|---|---|---|
| Station → controller | `telemetry`, `detection`, `command_result` | `emberflow/v0/stations/{station_id}/{message_type}` *(TBD)* |
| Controller → station | `fps_command`, `ack` | `emberflow/v0/stations/{station_id}/{message_type}` *(TBD)* |

## 2. Envelope

Every message uses this envelope:

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string | yes | `"0.1"` for this proposal |
| `event_id` | UUID string | yes | Assigned once at the source; **identical on replay**; dedup key |
| `message_type` | enum | yes | `telemetry` · `detection` · `fps_command` · `command_result` · `ack` |
| `station_id` | string `^[a-z0-9][a-z0-9-]{0,62}$` | yes | Sender for edge messages; target for controller messages |
| `source_timestamp` | RFC 3339 UTC (`…Z`) | yes | When the record was created at its source; **never rewritten** |
| `sequence` | integer ≥ 0 | no | *Proposal:* per-station monotonic counter to order delayed records |
| `payload` | object | yes | Shape depends on `message_type` |

The controller adds `received_at` when it stores a message. That value is not part of the
wire format.

## 3. Payloads

### 3.1 `telemetry` (station → controller)

| Field | Type | Notes |
|---|---|---|
| `cpu_percent` | number 0–100 | |
| `memory_percent` | number 0–100 | |
| `temperature_c` | number | SoC temperature |
| `inference_latency_ms` | number ≥ 0 | Recent mean/median; aggregation method TBD |
| `processing_fps` | number ≥ 0 | **Measured** processing rate (used to verify FPS commands) |
| `network_status` | `connected` · `degraded` · `disconnected` | As observed by the station when the record was created |
| `camera_status` | `ok` · `degraded` · `unavailable` | |
| `video_source_type` | `camera` · `file` | Optional |
| `active_model_version` | string | |

### 3.2 `detection` (station → controller)

| Field | Type | Notes |
|---|---|---|
| `prediction` | `smoke` · `no_smoke` | Whether `no_smoke` results are sent at all is TBD (bandwidth) |
| `confidence` | number 0–1 | |
| `model_version` | string | |
| `inference_latency_ms` | number ≥ 0 | |
| `snapshot_ref` | string \| null | **OPEN:** review imagery and offline snapshot handling |

### 3.3 `fps_command` (controller → station)

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | Unique per command; also the lifecycle key |
| `requested_fps` | number > 0 | No default value is approved |
| `created_at` | RFC 3339 UTC | |
| `expires_at` | RFC 3339 UTC | Station **must not apply** after this time |
| `policy_reason` | string | Human-readable trigger, e.g. which condition and window |

The target station is the envelope's `station_id`.

### 3.4 `command_result` (station → controller)

| Field | Type | Notes |
|---|---|---|
| `command_id` | UUID | |
| `state` | `accepted` · `applied` · `failed` | Stations cannot report `requested` or `verified` |
| `applied_fps` | number \| null | Actual FPS after applying |
| `detail` | string | Optional; required in practice for `failed` |

### 3.5 `ack`: durable acknowledgment (controller → station)

Sent **only after** the referenced records are committed to the database.

```json
{
  "results": [
    { "event_id": "…", "status": "stored" },
    { "event_id": "…", "status": "duplicate" }
  ]
}
```

| `status` | Meaning | Station action |
|---|---|---|
| `stored` | Newly committed | Remove from buffer |
| `duplicate` | Already stored earlier (replay) | Remove from buffer |
| `rejected` | Invalid; will never be accepted | Move to a dead-letter area and log it; do not retry forever |

If a station hears nothing back, it keeps the record and retries. Retrying is safe because of
deduplication. Batching rules and retry/backoff timing are TBD.

## 4. FPS command lifecycle

```
            (controller)          (station)          (station)          (controller)
 policy --> requested ----------> accepted --------> applied ----------> verified
               |                     |                  |                    
               +----> failed <-------+------------------+---- (no improvement / timeout)
```

| From → To | Trigger | Evidence recorded |
|---|---|---|
| — → `requested` | Policy condition held for the configured observation window; not in cooldown | Baseline telemetry window, policy config version, reason |
| `requested` → `accepted` | Station received the command before `expires_at` | `command_result` event |
| `requested` → `failed` | Expired before delivery, or explicitly rejected | `command_result` with detail, or controller timeout |
| `accepted` → `applied` | Station changed its processing FPS | `command_result` with `applied_fps` |
| `applied` → `verified` | Later telemetry shows `processing_fps` ≈ requested **and** improvement vs. baseline per success criteria | Post-change telemetry window and comparison result |
| `applied` → `failed` | No FPS change, or no measured improvement within the verification window | Comparison result |

Rules:

- One command per `command_id`. Stations handle duplicate deliveries idempotently.
- **Never apply an expired command**, including one replayed after a reconnect.
- **Cooldown/hysteresis:** no new FPS command for a station during its cooldown window. The
  rule for restoring FPS must not cause oscillation. *Whether and how FPS is restored is a
  policy detail for the team to decide.*
- Thresholds, windows, target FPS and success criteria are **OPEN** and come from Pi 5
  benchmarks.

## 5. REST API (controller ↔ dashboard), proposed

All endpoints are prefixed with `/api/v1`. JSON throughout.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/stations/register` | Station registration (if registration happens over REST rather than messaging; TBD with ADR 0004) |
| `GET` | `/stations` | List stations with health: `healthy` · `unhealthy` · `stale`, last seen, active model, current FPS |
| `GET` | `/stations/{station_id}` | Station detail |
| `GET` | `/stations/{station_id}/telemetry?from=&to=` | Telemetry history |
| `GET` | `/detections?station_id=&status=&from=&to=` | Potential smoke detections |
| `GET` | `/detections/{event_id}` | Detection detail |
| `POST` | `/detections/{event_id}/review` | Operator review: body `{ "decision": "confirmed" \| "dismissed", "note": "…" }` |
| `GET` | `/commands?station_id=` | FPS command audit list with lifecycle history |
| `GET` | `/commands/{command_id}` | Full audit: baseline, transitions, verification result |
| `GET` | `/health` | Controller liveness |

### Errors

Error format (proposal):

```json
{ "error": { "code": "station_not_found", "message": "Human-readable explanation" } }
```

| HTTP | When |
|---|---|
| 400 | Malformed request |
| 404 | Unknown station / detection / command |
| 409 | Conflict, e.g. reviewing an already-reviewed detection |
| 422 | Validation error (FastAPI default body may be adapted to the format above) |
| 503 | Database unavailable |

Authentication for the dashboard/API is **not yet designed** (prototype on a team-controlled
network). Record the decision in an ADR before exposing the API beyond that network.

## 6. Change process

1. Open a `docs(contracts)` or `feat(contracts)` PR that updates this file, the JSON Schema,
   and the example messages together.
2. Bump `schema_version` for any breaking change.
3. Get approval from the reviewers in CONTRIBUTING.md.
