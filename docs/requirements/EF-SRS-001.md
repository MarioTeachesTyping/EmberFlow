# EF-SRS-001: EmberFlow Software Requirements Specification

| | |
|---|---|
| **Document status** | **DRAFT — PENDING APPROVAL** |
| **Baseline** | Not baselined |
| **Approvals required** | All six team members (R1–R6) |
| **Precondition for baseline** | Decision register has owners and target dates for every open item |

> This draft was updated to match the architecture handoff dated 14 October 2026. That
> handoff reflects the Early Status Report MVP, the three-Pi-5 decision, PostgreSQL +
> TimescaleDB, and required FPS adaptation.
>
> **Requirement IDs below are provisional (`EF-*`).** The original SRS functional requirement
> IDs must be mapped to them **individually** by the team, using the "Original FR" column. That
> mapping was not available when this draft was written and has not been made up.

## 1. Purpose and scope

EmberFlow is a budget-conscious, two-semester research prototype. It aims to show reliable
wildfire smoke monitoring at the edge across changing device, network and visual conditions.
Its contribution is the integration of local inference, health monitoring, offline continuity,
human review and measured recovery. It is not a new smoke detector.

## 2. Functional requirements (required MVP)

| ID | Requirement | Original FR | Owner | Evidence of completion | Review |
|---|---|---|---|---|---|
| EF-FR-01 | Three Raspberry Pi 5 stations take part in one integrated system. | TBD | R2 | Three-node demo log | ☐ |
| EF-FR-02 | Each station processes a live camera stream **or** a prerecorded wildfire video. | TBD | R2 | Test run per source type | ☐ |
| EF-FR-03 | Each station runs smoke inference **locally**. | TBD | R2/R3 | Edge inference logs | ☐ |
| EF-FR-04 | The system provides one primary smoke-detection model and one lightweight/optimized alternative, starting from existing/pretrained architectures. | TBD | R3 | Model cards; benchmark report | ☐ |
| EF-FR-05 | Every inference result exposes prediction, confidence, model version and inference latency. | TBD | R3 | Contract test | ☐ |
| EF-FR-06 | Stations report telemetry: CPU, memory, temperature, inference latency, throughput/FPS, network status, camera status, active model version. | TBD | R2 | Contract test; DB records | ☐ |
| EF-FR-07 | The controller supports station registration. | TBD | R4 | API/integration test | ☐ |
| EF-FR-08 | The controller ingests telemetry and detection events. | TBD | R4 | Integration test | ☐ |
| EF-FR-09 | The controller identifies stale or unhealthy stations and tracks health. | TBD | R4 | Fault-injection test | ☐ |
| EF-FR-10 | The controller exposes API access to station, detection, telemetry and command data. | TBD | R4 | API tests | ☐ |
| EF-FR-11 | The dashboard shows station status. | TBD | R5 | UI test / demo | ☐ |
| EF-FR-12 | The dashboard shows potential smoke detections with confidence, time, station and model. | TBD | R5 | UI test / demo | ☐ |
| EF-FR-13 | Operators can confirm or dismiss alerts. | TBD | R5 | UI + API test | ☐ |
| EF-FR-14 | The dashboard shows relevant recent history. | TBD | R5 | UI test / demo | ☐ |
| EF-FR-15 | Data is stored persistently in PostgreSQL, with TimescaleDB for telemetry. | TBD | R5 | Migration + integration test | ☐ |
| EF-FR-16 | Event identifiers and source timestamps survive delayed delivery. | TBD | R2/R4/R5 | Replay test | ☐ |
| EF-FR-17 | During connectivity loss, inference continues locally. | TBD | R2 | Fault-injection test | ☐ |
| EF-FR-18 | During connectivity loss, detection and telemetry records are buffered durably and replayed on reconnection **with no duplicate accepted records**. | TBD | R2/R4 | Fault-injection test with dedup count | ☐ |
| EF-FR-19 | The system automatically reduces inference processing FPS when a defined degraded-resource condition persists. | TBD | R4/R2 | FPS adaptation experiment | ☐ |
| EF-FR-20 | For each FPS adaptation, the system records the initial condition, command, application and measured result (lifecycle: requested → accepted → applied → verified/failed or equivalent). | TBD | R4 | Command audit records | ☐ |
| EF-FR-21 | FPS adaptation uses a cooldown/hysteresis rule and never applies expired commands. | TBD | R4/R2 | Fault-injection test | ☐ |

## 3. Nonfunctional requirements

| ID | Requirement | Owner | Evidence | Review |
|---|---|---|---|---|
| EF-NFR-01 | Reliability tests are reproducible (scripted setup, documented configs). | R6 | `experiments/` configs + scripts | ☐ |
| EF-NFR-02 | ML evaluation reports precision, recall, F1 and false-alert rate for both model configurations. | R3 | Evaluation report | ☐ |
| EF-NFR-03 | Edge inference performance (latency, throughput) is measured on Raspberry Pi 5. | R3/R2 | Benchmark report | ☐ |
| EF-NFR-04 | Models are evaluated on a small, team-agreed set of degraded image inputs. | R3/R6 | Evaluation report | ☐ |
| EF-NFR-05 | FPS policy thresholds, windows, target FPS, cooldown and success criteria are derived from measurements on the selected Pi 5 configuration. | R4/R2/R6 | Benchmark data + ADR | ☐ |
| EF-NFR-06 | Every team member can run a simulated station with prerecorded input locally; physical Pis are needed only for hardware acceptance tests. | R1/R2 | Documented, verified procedure | ☐ |
| EF-NFR-07 | No secrets, large datasets or model weights in the repository. | All | CI / review checklist | ☐ |
| EF-NFR-08 | The adaptive behaviour is compared against simpler fixed/threshold-based behaviour. | R6 | Evaluation report | ☐ |
| EF-NFR-09 | The system runs without project funding: three Pi 5s plus a team-owned computer. No paid cloud services required. | R1 | Deployment doc | ☐ |

## 4. Stretch goals (not required for MVP acceptance)

| ID | Stretch goal |
|---|---|
| EF-SG-01 | Continuous image-quality monitoring (blur, fog, low light, scene change). *Degraded-image evaluation (EF-NFR-04) is still required.* |
| EF-SG-02 | Automatic resolution adjustment. |
| EF-SG-03 | Automatic model switching. |
| EF-SG-04 | Live active-vs-candidate model disagreement monitoring and shadow inference. |
| EF-SG-05 | Candidate/canary deployment orchestration. |
| EF-SG-06 | Automatic or operator-triggered rollback. |
| EF-SG-07 | Workload migration between Raspberry Pis. |

Original SRS requirements that covered these features must be **re-labelled as stretch goals**,
not deleted, so the change can be traced.

## 5. Exclusions (out of scope)

Drone integration; autonomous model retraining; certified life-safety and emergency dispatch;
production forest-wide deployment; novel ML architecture research; Kubernetes/cloud
orchestration as a requirement; unrestricted AI-agent control of physical devices.

## 6. Dependencies on open decisions

| Decision | Affects |
|---|---|
| Messaging MQTT vs NATS (ADR 0004) | EF-FR-07, 08, 18, 19–21 |
| Edge buffer implementation (ADR 0005) | EF-FR-17, 18 |
| Offline alert snapshots | EF-FR-12, 13, 18 |
| ML baseline and dataset (ADR 0006) | EF-FR-04, 05; EF-NFR-02–04 |
| FPS thresholds and evaluation | EF-FR-19–21; EF-NFR-05 |

## 7. Review and approval record

| Role | Name | Reviewed (date) | Approved |
|---|---|---|---|
| R1 | Anthony | | ☐ |
| R2 | Tomiwa | | ☐ |
| R3 | Diego | | ☐ |
| R4 | Gabe | | ☐ |
| R5 | Ethan | | ☐ |
| R6 | Dylan | | ☐ |

This document stays **DRAFT** until every row above is approved and every decision-register
entry has an owner and target date.
