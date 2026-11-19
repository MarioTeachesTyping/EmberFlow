# Interface contracts: Proposal v0.2

> **DRAFT FOR REVIEW — not agreed.** This proposes the next version of the edge message
> contract. [Proposal v0](contracts.md) stays in force until this is approved. Nothing here is
> implemented. Placeholders are marked; [Decisions for reviewers](#9-decisions-for-reviewers)
> lists what the owners need to settle.

- **Machine-readable schema:** [`schemas/edge-messages.v0.2.schema.json`](schemas/edge-messages.v0.2.schema.json) (JSON Schema 2020-12)
- **Example messages:** `testing/fixtures/contracts/v0.2/valid/` and `.../invalid/`, checked by
  `testing/unit/test_edge_message_schema_v0_2.py`
- **Prepared by:** R1 Anthony Terry. **Required reviewers** ([CONTRIBUTING.md](../../CONTRIBUTING.md#cross-subsystem-changes)):
  R1 + R2 Tomiwa (edge) + R4 James (controller). Requested: R3 Diego for `model_info` and
  `detection`; R5 Ethan for the error format, which the REST API shares.

## 1. Scope

This version covers the interface-contracts ticket: a common envelope, stale-state protection,
schemas for station status, telemetry, detections, model info and control commands, and an
agreed error format. Schemas stay version-controlled in `docs/api/` (SRS SI-1.5).

**Out of scope** (still tracked in the [v0 gap table](contracts.md#7-gaps-before-v11-integration)):
representative-image upload, integrity and complete durable receipt (SI-1.7, DR-1.7), which
depend on the open parts of SRS OD 2; trust-monitoring outputs and candidate comparison
records (FR-3.5–FR-3.7, FR-6.x); workload movement commands (FR-5.4, OD 7); the ML/edge frame
contract (SI-1.6); operator access and authorization.

## 2. Changes from v0

| Area | v0 | v0.2 |
|---|---|---|
| `schema_version` | `"0.1"` | `"0.2"` |
| Session identity | None | `session_id` (UUID per agent start), required on station messages |
| `sequence` | Optional | Required on station messages; per session, starts at 0 |
| Station status | None | New `station_status`: registration on startup, heartbeat, shutdown |
| Model info | Version string only | New `model_info`: active/candidate/fallback models with deployment IDs |
| Commands | `fps_command` only | Generic `command` with `command_type`: `set_fps`, `set_resolution`, `switch_model` |
| Command results | `applied_fps`, free-text `detail` | `applied` object; `error` object required when `failed` |
| Detection | No frame identity | `frame_id` required (DR-1.2) |
| Telemetry | — | Optional placeholders `storage_status`, `clock_synchronized` (DR-1.3) |
| Errors | REST body only; `ack` rejection had free text | One shared `error` object for messages and REST; required on `rejected` acks |

v0.2 is a breaking change. v0 messages are rejected by the v0.2 schema.

## 3. Transport

Messages are JSON bodies carried in MQTT publishes to the Mosquitto broker
([ADR 0004](../decisions/0004-messaging.md)). Reliability does not depend on MQTT QoS: it comes
from stable `event_id`s, store-then-ack at the controller, and deduplication.

Placeholder topics, **not agreed** (see question Q6):

| Direction | Message types | Placeholder topic |
|---|---|---|
| Station → controller | `station_status`, `telemetry`, `detection`, `model_info`, `command_result`, `error` | `emberflow/stations/{station_id}/{message_type}` |
| Controller → station | `command`, `ack` | `emberflow/stations/{station_id}/{message_type}` |

## 4. Envelope

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string | yes | `"0.2"` |
| `event_id` | UUID | yes | Assigned once at the source; identical on replay; dedup key |
| `message_type` | enum | yes | See §5 |
| `station_id` | string `^[a-z0-9][a-z0-9-]{0,62}$` | yes | Sender for station messages; **target station** for `command` and `ack` |
| `session_id` | UUID | station messages | New value each time the edge agent starts |
| `sequence` | integer ≥ 0 | station messages | Incremented for every station message in the session; preserved on replay |
| `source_timestamp` | RFC 3339 UTC (`…Z`) | yes | Creation time at the source; never rewritten |
| `payload` | object | yes | Shape depends on `message_type` |

**Stale-state protection (SI-1.8).** The controller tracks the latest `(session_id, sequence)`
per station. A message from an older session, or with a sequence at or below the latest seen
in the current session, is history: it is stored but does not update current station state.
Current liveness comes from fresh `station_status` heartbeats, not replayed records (FR-1.3).
The controller adds `received_at` when storing; it is not part of the wire format.

## 5. Message types

| `message_type` | Direction | Purpose | SRS |
|---|---|---|---|
| `station_status` | Station → controller | Registration (`startup`), heartbeat, `shutdown` | FR-1.1, FR-1.2, DR-1.1 |
| `telemetry` | Station → controller | Resource and pipeline metrics | DR-1.3, SI-1.8 |
| `detection` | Station → controller | Inference result | FR-2.3, DR-1.2 |
| `model_info` | Station → controller | Loaded models, on startup and on change | SI-1.4, FR-2.4, FR-6.1 |
| `command` | Controller → station | Adaptation command | FR-5.1–FR-5.3 |
| `command_result` | Station → controller | Command lifecycle report | FR-5.5 |
| `ack` | Controller → station | Metadata receipt per `event_id` | — |
| `error` | Station → controller | Error not tied to a command | — |

## 6. Payloads

Exact types and limits are in the schema; this section lists the fields.

**`station_status`:** `reason` (`startup` · `heartbeat` · `shutdown`), `agent_version`,
`hardware_revision`, `config_revision` (optional), `active_model_version`, `camera_status`,
`video_source_type` (optional), `heartbeat_interval_s`, `uptime_s` (optional). The station does
not report connected/degraded/offline/recovering; the controller derives that state.

**`telemetry`:** unchanged from v0, plus optional placeholders `storage_status`
(`ok` · `low` · `full`; thresholds depend on OD 9) and `clock_synchronized` (boolean).

**`detection`:** `frame_id`, `prediction`, `confidence`, `model_version`,
`inference_latency_ms`, `snapshot_ref` (unchanged from v0; see §1 out of scope).

**`model_info`:** `reason` (`startup` · `changed`) and `models`, a list with exactly one
`active` entry. Each entry has `model_version`, `role` (`active` · `candidate` · `fallback`),
`deployment_id` (null only for a model present before any recorded deployment), and optional
`artifact_sha256` and `runtime`.

**`command`:** `command_id`, `command_type`, `parameters`, `created_at`, `expires_at`,
`reason`. Parameters by type:

| `command_type` | `parameters` | SRS |
|---|---|---|
| `set_fps` | `requested_fps` > 0 | FR-5.1 |
| `set_resolution` | `width`, `height` (pixels) | FR-5.2 |
| `switch_model` | `model_version`, `deployment_id` | FR-5.3 |

**`command_result`:** `command_id`, `state` (`accepted` · `applied` · `failed`), `applied`
(values now in effect, same keys as `parameters`), `error` (required when `failed`).

**`ack`:** `results`, each with `event_id`, `status` (`stored` · `duplicate` · `rejected`) and
`error` (required when `rejected`). Still a metadata receipt only; it does not authorize image
cleanup (SI-1.7).

**`error`:** `component` (`agent` · `video` · `inference` · `telemetry` · `buffer` ·
`messaging`), optional `related_event_id`, and `error`.

## 7. Command lifecycle

The [v0 FPS lifecycle](contracts.md#4-fps-command-lifecycle) now applies to every
`command_type`: `requested` → `accepted` → `applied` → `verified`, with `failed` from any step.
`requested`, `verified` and `expired` are recorded by the controller; stations report only
`accepted`, `applied` and `failed`. Stations must never apply a command after `expires_at`,
and they handle duplicate deliveries of the same `command_id` idempotently.

## 8. Error format

One error object is used everywhere: in `command_result`, `ack`, `error` messages, and as the
REST error body `{"error": {...}}`.

```json
{
  "code": "command_expired",
  "message": "Command received after expires_at; not applied.",
  "retryable": false,
  "details": {}
}
```

| Field | Notes |
|---|---|
| `code` | Stable snake_case identifier; clients branch on this, never on `message` |
| `message` | Human-readable explanation |
| `retryable` | Whether the sender may retry the same request unchanged |
| `details` | Optional object with extra context |

Initial codes (the list is open for additions; see Q4):

| Code | Used by | Meaning |
|---|---|---|
| `invalid_message` | station, controller | Message could not be parsed |
| `schema_validation_failed` | station, controller | Message parsed but failed schema validation |
| `unsupported_schema_version` | station, controller | `schema_version` not supported |
| `command_expired` | station | Command received after `expires_at` |
| `command_unsupported` | station | `command_type` not supported by this station |
| `invalid_parameters` | station | Parameters outside what the station can apply |
| `model_not_available` | station | `switch_model` target not present or not approved |
| `camera_unavailable` | station | Video input lost |
| `inference_failed` | station | Model failed to produce a result |
| `storage_full` | station | Local storage cannot admit new records |
| `internal_error` | station, controller | Unexpected failure |
| `not_found` | REST | Unknown station, detection or command |
| `conflict` | REST | E.g. reviewing an already-reviewed detection |
| `database_unavailable` | controller, REST | Storage temporarily unavailable |

REST keeps the v0 HTTP status mapping (400, 404, 409, 422, 503).

## 9. Decisions for reviewers

| # | Question | Proposed in this draft | Owner |
|---|---|---|---|
| Q1 | Is `session_id` a fresh UUID per agent start? | Yes | R2, R4 |
| Q2 | Is `sequence` shared across all of a station's message types, resetting each session? | Yes, one counter per session | R2, R4 |
| Q3 | Should `command` and `ack` also carry `session_id` to target a specific station session? | No | R4 |
| Q4 | Error codes: open snake_case set with a documented registry, or a fixed enum? | Open set plus registry (§8) | R4, R5 |
| Q5 | Is `heartbeat_interval_s` the right way to share heartbeat timing, and what is the default? | Field included; no default | R2, R4 |
| Q6 | MQTT topic names, QoS level per message type, retained messages, version in topic? | Placeholder topics only | R4 |
| Q7 | Which command types belong in v0.2? Should `move_workload` wait for OD 7? | `set_fps`, `set_resolution`, `switch_model`; workload later | R4, R2 |
| Q8 | `frame_id` format, and is it enough frame identity for DR-1.2? | Free string | R2, R3 |
| Q9 | `model_info` fields: are `artifact_sha256` and `runtime` useful, and is the `fallback` role right? | Optional fields; three roles | R3, R4 |
| Q10 | Should `no_smoke` detections be sent at all (bandwidth)? | Unchanged from v0: allowed | R3, R4 |

## 10. Adoption

When approved: fold this document into [contracts.md](contracts.md), replace the v0 schema
and fixtures, update the [v0 gap table](contracts.md#7-gaps-before-v11-integration), and record
the approval in the PR. Until then, v0 remains the reference.
