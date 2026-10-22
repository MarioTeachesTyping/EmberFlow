<h1 align="center">EmberFlow</h1>

<p align="center">Distributed edge-computing research prototype for reliable wildfire smoke monitoring.</p>

Project documents and agent context: start with [docs/PROJECT_REFERENCE.md](docs/PROJECT_REFERENCE.md).
It links the October 22 v1.1 review specifications and the [repository audit](docs/reviews/2026-10-22-repository-audit.md).
Agents should also read the root [AGENTS.md](AGENTS.md).

> **Project status: Phase 1 — Foundation.** This repository currently contains the scaffold,
> standards, documentation and a *proposed* message contract. **No runnable EmberFlow subsystem
> (edge agent, ML inference, controller, database, dashboard) is present in this checkout.**
> See [Implemented vs planned](#implemented-vs-planned).

EmberFlow is a two-semester senior-design project by six students: one Computer Engineering
student and five Computer Science students. No hardware budget or funding plan has been agreed,
and no purchased hardware is established by the reviewed sources.

## Problem and research goal

Wildfire smoke monitoring at the edge has to keep working as device, network and visual
conditions change. EmberFlow's contribution is **not** a new state-of-the-art smoke detector.
It aims to show that the following can work together and be measured:

- local smoke inference on Raspberry Pi 5 stations,
- health monitoring of those stations,
- offline continuity (buffering and replay without duplicates),
- human review of potential detections,
- image/model trust monitoring, candidate evaluation and controlled model deployment, and
- measured, audited adaptation and recovery under recorded fault conditions.

## Scope

### Current review scope

The [v1.1 system SRS](docs/specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md) is the
current review baseline. Tomiwa approved aligning this repository to that scope on October 22;
full-team/faculty approval is still pending. The earlier reduced MVP/stretch split is historical.
The first vertical slice is a delivery milestone, not the complete acceptance scope.

- **Hardware/platform:** three physical Raspberry Pi 5 stations for an indoor demonstration;
  no custom PCB. One USB webcam initially, to be tested on each station in turn; local prerecorded
  input on the other two stations. Wired Ethernet connects the Pis and an existing team computer.
- **Local inference:** primary and lightweight/optimized model configurations with versioned
  prediction, confidence, source/frame identity, and inference latency. Model/runtime selection
  and Pi measurements remain open.
- **Monitoring:** device health, camera/network/storage status, image quality, input change,
  and meaningful model disagreement. Diego owns the methods; Tomiwa integrates edge execution.
- **Offline evidence:** continue local processing, retain accepted event metadata with one
  representative image plus retained telemetry, and replay safely. Completion requires durable,
  jointly reviewable metadata and image centrally. Bound capacity and expose admission failures.
- **Controller and operator:** registration, ingestion, state/freshness tracking, human alert
  review, configurable limits, model approval/deployment controls, and actor/trigger/outcome audit.
- **Adaptation/model lifecycle:** FPS and resolution control, approved smaller-model switching,
  workload movement with an accessible input source, shadow comparison, limited rollout, and
  restoration of a known-good model. AC-4 requires three demonstrated mechanisms; it does not
  waive the individual mandatory requirements for the others.
- **Persistence:** PostgreSQL with TimescaleDB, with versioned station, evidence, telemetry,
  deployment, review, and audit records. Exact image storage and completion protocol remain open.
- **Evaluation:** fixed deployment vs simple temperature threshold vs full EmberFlow using
  comparable inputs/faults; detection quality, input-change timing, availability, recovery,
  latency, buffered-alert delivery, and rollback metrics.
- **Handoff/acceptance:** another teammate reproduces the supported station; final hardware,
  model, interface, storage and numerical test profiles are frozen before qualification.

### Out of scope

Drone integration; autonomous model retraining; certified life-safety or emergency dispatch;
production forest-wide deployment; novel ML architecture research; Kubernetes/cloud
orchestration as a requirement; unrestricted AI-agent control of physical devices. These stay
out of the backlog unless the team formally revises scope.

## Implemented vs planned

| Component | State |
|---|---|
| Repository scaffold, standards, CI | **Present** |
| Edge message contract (JSON Schema) + fixture tests | **Present — legacy PROPOSAL v0**, incomplete for v1.1; see [contract gaps](docs/api/contracts.md#7-gaps-before-v11-integration) |
| Architecture, deployment, contracts, SRS, ADR, test-plan docs | **Present — drafts** |
| Edge agent, telemetry, video, offline buffer | Planned |
| ML models, inference, evaluation | Planned (model choice OPEN) |
| Controller API, messaging, adaptation, candidate rollout/rollback, migration | Planned (protocols and policy details OPEN) |
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
per-frame inference. This is a logical architecture; the physical baseline is wired Ethernet on a team-controlled LAN. Details:
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

These commands verify the repository tooling and example schemas, not the planned EmberFlow services.

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

Optional agent navigation: [Graphify setup and limits](docs/tooling/graphify.md). It complements
the project reference and runs in a separate developer environment; it is not required by CI.

GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs Ruff lint, Ruff
format check and pytest on every PR and on pushes to `main`. Dashboard lint/typecheck/test/build
steps turn on automatically once `dashboard/frontend/package.json` and its lockfile exist. See
[docs/testing/test-plan.md](docs/testing/test-plan.md).

## Team roles

| Role | Member | Owns |
|---|---|---|
| R1 | Anthony Terry | Architecture, cross-team schemas, repository standards, integration and release coordination |
| R2 | Tomiwa Aluko | Edge hardware/platform, video, telemetry, durable metadata/image buffering, valid command execution and platform handoff |
| R3 | Diego Mendoza | Datasets, models, inference contract, trust-monitoring methods, candidate comparison and benchmarks |
| R4 | James Connolly | Controller, messaging/ingestion, freshness, adaptation, deployment/rollback, workload coordination, durable receipt |
| R5 | Ethan McKissic | Central persistence/images, dashboard, alert review, configuration/model approval and audit history |
| R6 | Dylan Mcintee | CI, automated tests, fault injection, repeatable experiments, reliability metrics |

James also appears as Gabe/Gabriel in source material and Jira; use James Connolly in formal documents.
Subsystem owners stay responsible for testing their own code. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.

## Implementation phases

1. **Foundation:** repository, standards, shared schemas, scope/SRS review, decision register, CI. *(in progress)*
2. **Vertical slice:** one real or simulated station → controller → database → dashboard, with real or mocked inference.
3. **Three-node integration:** physical Pis, common USB camera support, telemetry, reviewable offline metadata/images, and teammate platform handoff.
4. **Trust/adaptation/model lifecycle:** image/input-change/disagreement methods, control mechanisms, accessible-source workload movement, candidate comparison, limited rollout, rollback and audit.
5. **Qualification and evaluation:** freeze measured targets; run all individual requirements and acceptance gates, including the three-controller comparison.

Procurement first needs an equipment inventory, budget and BOM. Benchmark one Pi with Diego
before freezing remaining station variants and performance commitments. SD1 emphasizes design,
comparisons and available bench evidence; SD2 closes the integrated implementation/evaluation.
Use the SRS milestone gates and reconcile the CS-led calendar with Tomiwa's separate ECE
writing/evaluation obligations. The no-PCB clarification does not waive those obligations.

## License

No license has been chosen yet. One will be added only after the team explicitly chooses it.
