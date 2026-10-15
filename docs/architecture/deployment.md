# Deployment

**Status:** Draft plan. Nothing here has been deployed or verified yet.
**Owner:** R1 (Anthony), with R2 (edge) and R4/R5 (central services).

## 1. Topology assumptions

- **Edge:** exactly three Raspberry Pi 5 devices, each a station with its own camera or
  prerecorded video source.
- **Central host:** one **team-owned computer** runs the controller, database, messaging
  infrastructure and dashboard. Cloud hosting is not required.
- **Network:** the Pis and the central host share a network the team controls (lab LAN or
  similar). The exact physical layout is **not decided**.
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
| Offline buffer | Durable local store (SQLite recommended) | File on local storage |

Still to decide or record: Pi OS version, Python version on the Pi, camera hardware, the
process supervisor (e.g. systemd), and cooling setup. Cooling directly affects the
temperature trigger.

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

Rollout to the Pis (copying code and models, managing services) is still to be designed. Use
a simple, documented manual or scripted procedure. Canary/rollback orchestration is a
**stretch goal**.

## 6. To be documented once verified

- [ ] Exact Pi OS image and Python version
- [ ] Camera model(s) and how each station's camera is configured
- [ ] Central host OS and Docker setup
- [ ] Broker setup (after ADR 0004)
- [ ] Commands that have been run and verified to bring up the full stack
