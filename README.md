<h1 align="center">EmberFlow</h1>

<p align="center">Distributed edge-computing research prototype for reliable wildfire smoke monitoring.</p>

Project documents and agent context: start with [docs/PROJECT_REFERENCE.md](docs/PROJECT_REFERENCE.md).
It links the October 22 v1.1 specifications and identifies unresolved differences from this
repository's earlier MVP draft. Agents should also read the root [AGENTS.md](AGENTS.md).

> **Project status: Phase 1 — Foundation.** This repository currently contains the scaffold,
> standards, documentation and a *proposed* message contract. **No EmberFlow subsystem
> (edge agent, ML inference, controller, database, dashboard) has been implemented yet.**
> See [Implemented vs planned](#implemented-vs-planned).

EmberFlow is a two-semester senior-design project by a six-person team with no project funding.

## Problem and research goal

Wildfire smoke monitoring at the edge has to keep working as device, network and visual
conditions change. EmberFlow's contribution is **not** a new state-of-the-art smoke detector.
It aims to show that the following can work together and be measured:

- local smoke inference on Raspberry Pi 5 stations,
- health monitoring of those stations,
- offline continuity (buffering and replay without duplicates),
- human review of potential detections, and
- measured, audited recovery: specifically **automatic inference frame-rate reduction** when a
  defined degraded-resource condition persists.

## Scope

### Required MVP

- **Three Raspberry Pi 5 stations** in one integrated system, each processing a live camera or
  prerecorded wildfire video and running inference locally.
- **Two model configurations:** one primary smoke-detection model and one lightweight/optimized
  alternative, each reporting prediction, confidence, model version and inference latency.
  Both start from existing pretrained architectures.
- **Edge telemetry:** CPU, memory, temperature, inference latency, throughput/FPS, network
  status, camera status, active model version.
- **Controller (Python/FastAPI):** station registration, telemetry/detection ingestion,
  stale/unhealthy station detection, health tracking, API access.
- **Operator dashboard (React + TypeScript):** station status, potential smoke detections with
  confidence/time/station/model, confirm/dismiss alerts, recent history.
- **Central storage:** PostgreSQL with TimescaleDB for telemetry. Event IDs and source
  timestamps survive delayed delivery.
- **Offline continuity:** inference continues during connectivity loss. Records are durably
  buffered and replayed on reconnection, and no record is accepted twice.
- **Required automated adaptation:** automatic inference FPS reduction under a sustained
  degraded-resource condition, with the initial condition, command, application and measured
  result all recorded.
- **Evaluation:** reproducible reliability tests; precision, recall, F1, false-alert rate and
  edge inference performance; evaluation on a small agreed set of degraded image inputs.

### Stretch goals (not mandatory)

- Continuous image-quality monitoring (blur/fog/low light/scene change). Degraded-image
  *evaluation* is still required.
- Automatic resolution adjustment and automatic model switching.
- Live active-vs-candidate model disagreement monitoring and shadow inference.
- Candidate/canary deployment and automatic or operator-triggered rollback.
- Workload migration between Raspberry Pis.

### Out of scope

Drone integration; autonomous model retraining; certified life-safety or emergency dispatch;
production forest-wide deployment; novel ML architecture research; Kubernetes/cloud
orchestration as a requirement; unrestricted AI-agent control of physical devices. These stay
out of the backlog unless the team formally revises scope.

## Implemented vs planned

| Component | State |
|---|---|
| Repository scaffold, standards, CI | **Present** |
| Edge message contract (JSON Schema) + fixture tests | **Present — PROPOSAL v0**, pending team review |
| Architecture, deployment, contracts, SRS, ADR, test-plan docs | **Present — drafts** |
| Edge agent, telemetry, video, offline buffer | Planned |
| ML models, inference, evaluation | Planned (model choice OPEN) |
| Controller API, messaging, FPS policy, command lifecycle | Planned (messaging OPEN) |
| Database schema and migrations | Planned |
| Operator dashboard | Planned (project not yet initialized) |
| Fault injection and experiments | Planned |

## Logical architecture

```
[Operator: React + TypeScript dashboard]
              | REST API
              v
[Central Controller: FastAPI] <----> [PostgreSQL + TimescaleDB]
              |
     MQTT or NATS (OPEN DECISION)
   telemetry, detections, commands
              |
   +----------+----------+
   |          |          |
[Pi 5 #1]  [Pi 5 #2]  [Pi 5 #3]
video+ML   video+ML   video+ML
telemetry  telemetry  telemetry
buffer     buffer     buffer
FPS ctl    FPS ctl    FPS ctl
```

Inference runs on the Pis. The controller handles policy and collects events; it does not run
per-frame inference. This is a logical architecture, not a fixed network layout. Details:
[docs/architecture/overview.md](docs/architecture/overview.md).

## Technology baseline

| Area | Decision | Status |
|---|---|---|
| Edge hardware | 3 × Raspberry Pi 5 (no Jetson) | Accepted — [ADR 0001](docs/decisions/0001-edge-hardware.md) |
| Database | PostgreSQL + TimescaleDB | Accepted — [ADR 0002](docs/decisions/0002-central-database.md) |
| Controller / dashboard | Python FastAPI / React + TypeScript | Accepted — [ADR 0003](docs/decisions/0003-central-services-stack.md) |
| Messaging | MQTT **or** NATS | **OPEN** — [ADR 0004](docs/decisions/0004-messaging.md) |
| Edge offline buffer | SQLite recommended | **Proposed** — [ADR 0005](docs/decisions/0005-edge-offline-buffer.md) |
| ML baseline and dataset | Lightweight pretrained candidates | **OPEN** — [ADR 0006](docs/decisions/0006-ml-baseline.md) |

Python ≥ 3.11 for shared tooling. The full decision register is in
[docs/decisions/README.md](docs/decisions/README.md).

## Repository layout

| Path | Purpose | Owner |
|---|---|---|
| [`edge/`](edge/) | Pi 5 agent, telemetry, video input, offline buffer | R2 |
| [`ml/`](ml/) | Models, training, inference interface, evaluation | R3 |
| [`controller/`](controller/) | FastAPI app: API, messaging, policies, recovery | R4 |
| [`dashboard/`](dashboard/) | React + TypeScript operator UI | R5 |
| [`data/`](data/) | PostgreSQL/TimescaleDB schema and migrations | R5 |
| [`testing/`](testing/) | Unit, integration, fault-injection tests and fixtures | R6 |
| [`infrastructure/`](infrastructure/) | Docker and Pi/central-host deployment | R1 + owners |
| [`experiments/`](experiments/) | Reproducible experiment configs, scripts, local results | R6 |
| [`docs/`](docs/) | Architecture, requirements, API, ADRs, testing, research | R1 + all |

Each directory has a README that states its owner, planned contents and boundaries.

## Development

Everything in this section has been run and verified.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux/Pi: source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest
```

`pytest` currently checks the proposed edge message schema against the example messages in
`testing/fixtures/contracts/`.

There is **no run/quickstart for EmberFlow itself yet**, because no runnable service exists.
Once Phase 2 lands, the goal is that every team member can run a simulated edge node with
prerecorded video on a laptop; physical Pis should only be needed for hardware acceptance tests.

## Tests and CI

GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs Ruff lint, Ruff
format check and pytest on every PR and on pushes to `main`. Dashboard lint/typecheck/test/build
steps turn on automatically once `dashboard/frontend/package.json` and its lockfile exist. See
[docs/testing/test-plan.md](docs/testing/test-plan.md).

## Team roles

| Role | Member | Owns |
|---|---|---|
| R1 | Anthony | Architecture, cross-team schemas, repository standards, integration and release coordination |
| R2 | Tomiwa | Pi 5 hardware, camera/video input, edge agent, metrics, edge-side FPS execution and buffering |
| R3 | Diego | Datasets, primary/alternative model, inference output contract, benchmarks, model evaluation |
| R4 | Gabe | FastAPI, registration, messaging, ingestion, node health, FPS policy, command lifecycle, replay acknowledgment |
| R5 | Ethan | PostgreSQL/TimescaleDB schema and migrations, dashboard, alerts, history, operator workflows |
| R6 | Dylan | CI, automated tests, fault injection, repeatable experiments, reliability metrics |

Subsystem owners stay responsible for testing their own code. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.

## Implementation phases

1. **Foundation:** repository, standards, shared schemas, scope/SRS review, decision register, CI. *(in progress)*
2. **Vertical slice:** one real or simulated station → controller → database → dashboard, with real or mocked inference.
3. **Three-node MVP:** all three Pi 5s, two model configurations, telemetry, operator alerts, offline buffering/replay.
4. **FPS adaptation:** trigger, command, apply, verify, cooldown, complete audit evidence.
5. **Evaluation:** repeatable failures, degraded-image evaluation, comparison against simpler fixed/threshold behaviour.

## License

No license has been chosen yet. One will be added only after the team explicitly chooses it.
