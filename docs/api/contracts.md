# Interface contracts

> **LEGACY PROPOSAL v0. Not approved; incomplete for v1.1.** This defines the *planned* edge event envelope, message
> payloads, FPS command lifecycle, durable acknowledgment and REST endpoints. Nothing here is
> implemented. Changes require the reviewers listed in
> [CONTRIBUTING.md § Cross-subsystem changes](../../CONTRIBUTING.md#cross-subsystem-changes).

- **Integration warning:** v0 fixtures validate the old shape only; see [required gaps](#7-gaps-before-v11-integration). Do not treat a metadata ack as complete image receipt.
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
| `snapshot_ref` | string \| null | Legacy v0 allows missing/null; v1.1 requires representative-image evidence. This field does not encode that full contract. |

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

Legacy v0 metadata receipt, sent after referenced records are committed to the database. It cannot by itself establish v1.1 metadata-plus-image completion.

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
| `stored` | Metadata newly committed | Legacy metadata receipt only; retain detection evidence pending complete image receipt |
| `duplicate` | Metadata stored earlier (replay) | Do not infer the image is complete; require complete evidence receipt |
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

## 7. Gaps before v1.1 integration

The schema, fixtures and enum remain Proposal v0; this sweep changes descriptions, not validation
rules. In particular, the old `model_switch` invalid fixture means "not a v0 message type," not
"model switching is out of project scope." A null-image valid fixture is legacy shape coverage,
not valid acceptance evidence for the revised system.

R1/R2/R3/R4/R5 must agree and version the following before a production integration contract:

| Gap | Required direction / source | Still to design |
|---|---|---|
| Registration/liveness | SRS FR-1.1–FR-1.3; SI-1.8; R2-FR-2.2 | Registration payload/transport, station/session/sequence, freshness and clock validity; no v0 heartbeat or registration message exists |
| Frame/model input/output | SI-1.6; FR-2.3; DR-1.2 | Frame ID, shape/layout/color order, preprocessing owner, runtime/dependencies, error and latency semantics |
| Detection image | SI-1.7; FR-7.2–FR-7.7; DR-1.7 | Image ID/event binding, encoding, byte count/integrity, upload transport, partial/restart handling, complete durable receipt |
| Capacity/telemetry | DR-1.3; R2-FR-6.7; R2-IF-04 | Storage/backlog/clock status and units; quota/reserve/admission/retention profile |
| Trust/model lifecycle | FR-3.5–FR-3.7; FR-6.1–FR-6.6 | Quality/change/disagreement outputs, paired candidate results, deployments, approval and rollback records |
| Non-FPS commands | FR-5.2–FR-5.5 | Resolution/model/worker/movement contracts, accessible source and correlated outcomes |
| Operator/configuration API | UI-1.3–UI-1.5; NFR-4.1–NFR-4.3 | Identified operator access, authorization, validation, configuration/model routes and audit |

An accepted local event needs persisted metadata and a recoverable image association. Central
ingestion can stage the parts separately, but exposes incomplete state until both are durable
and jointly retrievable. Receipt covers the whole evidence unit. Retries after lost receipts are
safe; local cleanup follows the selected post-receipt retention policy. A broker receipt, existing
event ID or HTTP success for metadata alone does not meet this requirement.

Retain transport independence while MQTT/NATS and image transfer remain open. Contract revisions
must update schemas and valid/invalid fixtures together and follow the reviewers in CONTRIBUTING.
These planning requirements do not silently add new fields to the existing v0 wire format.
