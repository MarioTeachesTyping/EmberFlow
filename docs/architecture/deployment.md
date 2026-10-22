# Deployment

**Status:** Draft plan. Nothing here has been deployed or verified yet.
**Owner:** R1 (Anthony), with R2 (edge) and R4/R5 (central services).

## 1. Topology assumptions

- **Edge:** three physical Raspberry Pi 5 stations with a common camera-capable platform.
  Initially one USB webcam, tested on each Pi in turn; local replay on the other two. No custom PCB.
- **Environment:** indoor demonstration, compatible mains supplies/cables, documented cooling
  and bounded storage. No outdoor enclosure, autonomous field power or UPS is promised.
- **Central host:** one **team-owned computer** runs the controller, database, messaging
  infrastructure and dashboard. Cloud hosting is not required.
- **Network:** wired Ethernet from the three Pis and existing central host to a switch/router
  with at least four endpoint ports. Exact equipment, host adapter, addresses/routes, broker/API
  ports and access controls are open. Do not assume an internet dependency for local inference.
- **Development:** every developer can run a **simulated station** with prerecorded video on
  a laptop. The physical Pis are only needed for hardware acceptance tests.

```
           team-owned central computer
 +--------------------------------------------------+
 | FastAPI controller | PostgreSQL + TimescaleDB    |
 | messaging broker (MQTT or NATS — OPEN)           |
 | dashboard (static React build served to browser) |
 +--------------------------------------------------+
            ^            ^            ^
            |   LAN      |            |
       [Pi 5 #1]    [Pi 5 #2]    [Pi 5 #3]
```

## 2. Processes on each Raspberry Pi 5

| Process / module | Purpose | Notes |
|---|---|---|
| Edge agent | Main station process; registration, messaging, command handling | One process with internal modules preferred |
| Video pipeline | Camera or file input at a controllable processing FPS | In-process module of the agent |
| Inference | Primary or lightweight model | In-process; model loaded from local path |
| Telemetry collector | System and pipeline metrics | In-process |
| Offline evidence | Durable metadata/image outbox and retained telemetry (SQLite proposed for metadata) | Image storage/lifecycle and quotas still to define |

Still to decide or record: Pi OS/Python/runtime versions, exact USB camera/modes, board RAM,
storage, compatible supplies/cables/cooling and service supervision. Inventory and budget precede
purchases. Benchmark one Pi with Diego before freezing variants and numerical targets. Record
physical connections, power/thermal observations and the per-station hardware/software revision.

## 3. Services on the central host

| Service | Technology | Status |
|---|---|---|
| Controller | Python FastAPI | Decided |
| Database | PostgreSQL + TimescaleDB | Decided |
| Messaging broker | MQTT broker **or** NATS server | **OPEN** |
| Dashboard | React + TypeScript (static build) | Decided; build tooling not chosen |
| Redis | — | Not required |

Containerizing these with Docker (`infrastructure/docker/`) is the expected approach. The
compose file will be added only once it has been written and actually run.

## 4. Configuration

- All runtime configuration comes from environment variables / `.env` files. The template is
  [`.env.example`](../../.env.example).
- Each Pi has its own `.env` with a unique `STATION_ID`.
- `MESSAGING_BACKEND` stays empty until ADR 0004 is accepted.
- FPS policy values are intentionally blank until benchmarked.
- Secrets (database passwords, broker credentials) live only in local `.env` files that are
  never committed.

## 5. Startup / deployment plan (proposed order)

1. Start central services: database → messaging broker → controller → dashboard.
2. Apply database migrations (tool still to be chosen; see `data/migrations/`).
3. Start each station's edge agent. It registers with the controller and begins publishing.
4. Check that each station shows as healthy on the dashboard.

Rollout to the Pis (copying code/models and supervising services) remains to be designed.
Version the setup, model adapter and dependency/configuration records; a non-owner teammate
must reproduce the platform. Candidate/shadow comparison, limited rollout and known-good
rollback are required in the v1.1 review scope. Workload movement requires a destination-accessible
source. Full-team/faculty ratification of the revised scope is pending; no deployment is claimed.

## 6. To be documented once verified

- [ ] Exact Pi OS image and Python version
- [ ] Camera model(s) and how each station's camera is configured
- [ ] Central host OS and Docker setup
- [ ] Broker setup (after ADR 0004)
- [ ] Commands that have been run and verified to bring up the full stack

- [ ] Representative-image persistence, integrity, receipt, retention and capacity profile
- [ ] Physical diagram/BOM/station inventory and teammate platform reproduction
- [ ] Supported algorithm/model-adapter fixture, frozen benchmark/acceptance profile

See [ADR 0007](../decisions/0007-october-22-review-baseline.md) and the
[audit](../reviews/2026-10-22-repository-audit.md) for the revision authority and remaining gaps.
