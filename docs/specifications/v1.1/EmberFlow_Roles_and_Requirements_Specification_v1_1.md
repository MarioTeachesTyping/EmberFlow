# EmberFlow Roles and Requirements Specification

Named subsystem ownership and shared integration requirements

EF-TEAM-001 | Revision 1.1 | October 22 2026 | Review draft

We organize EmberFlow around six named subsystem owners. This revision makes Tomiwa Aluko's physical hardware and platform contribution explicit and aligns the team's shared requirements with the three Pi 5 indoor demonstration and offline image-review evidence.

Revision 1.1 implements the hardware-focused document revision approved by Tomiwa on October 22, 2026. It is a review draft for faculty and team reconciliation. Requirements describe intended behavior; no procurement, trained model, hardware benchmark, or implementation result is asserted by this document.

### Document control

| Revision | Basis |
| --- | --- |
| 1.0 | Original attached specification; retained as the source baseline. |
| 1.1 | Named owners; Pi 5 indoor platform; USB camera and wired Ethernet; existing central host; offline image evidence; physical diagrams; interface and verification updates. |

Shall identifies an acceptance obligation; should identifies a recommendation; may identifies an option. A chosen architecture is distinguished from an unselected part or proposed implementation. The professor clarification that no custom PCB is required was reported by Tomiwa [S6]; it does not waive unrelated ECE coursework or writing obligations.

## 1 Project purpose

EmberFlow is a two-semester research prototype for reliable wildfire-smoke monitoring. It combines local inference, device and input/model health monitoring, controlled adaptation, human review, offline continuity, and comparative evaluation. Human verification remains essential. Autonomous retraining, drone integration, and certified dispatch are outside required scope.

## 2 System architecture and hardware baseline

| Area | Agreed revision scope |
| --- | --- |
| Physical stations | Three Raspberry Pi 5 edge stations; same supported platform configuration. |
| Live video | One USB webcam initially. Demonstrate that the same camera can operate on each station in turn. |
| Other video inputs | Local prerecorded wildfire footage on the other two stations and for repeatable comparisons. |
| Location | Indoor research demonstration with available mains power; remote outdoor deployment is not required. |
| Central host | An existing team laptop or desktop hosts controller, database, and dashboard services. |
| Network | Wired Ethernet local network through a suitable switch or router. |
| Offline evidence | Detection metadata, one representative image per detection event, and telemetry under a documented retention policy. |
| Custom circuitry | No custom PCB is required, per the professor clarification reported by Tomiwa. |
| Procurement status | No hardware purchased or firmly selected; no total hardware budget set at revision time. |
| Model status | Lightweight YOLO-family candidates and FIgLib research; no final model, trained artifact, or measured Pi benchmark documented in reviewed sources. |

![Figure 1. Physical deployment baseline and central-service boundary.](diagrams/system_deployment.png)

## 3 Named team structure

| Role | Member | Ownership |
| --- | --- | --- |
| R2 | Tomiwa Aluko | Edge hardware and embedded platform |
| R1 | Anthony Terry | Architecture and system integration |
| R3 | Diego Mendoza | Machine learning and computer vision |
| R4 | James Connolly | Backend and central controller |
| R5 | Ethan McKissic | Dashboard and shared persistence |
| R6 | Dylan Mcintee | Reliability and validation |

Tomiwa is the only Computer Engineering member; the other five members are Computer Science students. James also appears as Gabe or Gabriel in source documents and Jira. This revision uses James Connolly consistently for formal ownership. Ownership assigns accountability without excluding shared integration, testing, and documentation.

## 4 Anthony Terry system architecture and integration

Anthony owns overall architecture, interface coordination, repository and review standards, integration planning, release baselines, and technical risk. He coordinates project management and milestones while each owner remains accountable for technical completion. He reviews the hardware diagram and cross-subsystem contracts with Tomiwa, James, Diego, Ethan, and Dylan.

- Deliver architecture and deployment views, shared interface standards, integration sequence, release configuration, and risk register.
- Coordinate reviews and evidence readiness without transferring all implementation work to the integration lead.

## 5 Tomiwa Aluko edge hardware and embedded platform

Tomiwa owns selection, assembly, configuration, integration, measurement, and verification of the three physical Pi 5 stations. This includes power, cooling, local storage, one USB webcam, wired networking, camera/replay capture, edge execution environment, timestamped device telemetry, local metadata/image retention, synchronization client, command execution, and service recovery.

His hardware work shall be visible through component comparisons, a BOM, a physical block diagram, connection records, station inventory, and power/thermal/performance observations. His platform shall let teammates deploy agreed algorithms using documented frame/model/output contracts. No custom PCB is required for this interdisciplinary contribution, per the professor clarification reported by Tomiwa [S6].

![Figure 2. Tomiwa's station hardware and integration boundary.](diagrams/station_hardware.png)

- Hardware deliverables: three physical configured stations, one webcam verified across stations, BOM and selection rationale, supply/cooling/storage records, network and connection diagrams.
- Software deliverables: capture/replay pipeline, edge agent, telemetry, ML runtime adapter, controller command mechanisms, persistent event/image outbox, reconnect synchronization, model switching/rollback support, recovery, and logs.
- Handoff deliverables: setup/deployment guide, versioned interfaces and fixture, benchmark/test profile, troubleshooting, acceptance evidence, and a successful non-owner reproduction record.

Diego owns model and image-analysis development; James owns central policy and ingestion; Ethan owns central persistence and operator review. Tomiwa supplies reliable execution and evidence from physical devices. Detailed requirements and preserved R2 identifiers are in EF-R2-001 revision 1.1.

## 6 Diego Mendoza machine learning and computer vision

Diego owns dataset review and split design, baseline and lightweight/optimized model selection, training/fine-tuning, model artifacts and export path, prediction/confidence semantics, accuracy evaluation, image-quality methods, model disagreement, and visual input-change algorithms. He supplies model/runtime/preprocessing requirements to Tomiwa and validates the integrated model outputs.

The reviewed proposal names FIgLib and lightweight YOLO-family candidates and proposes Python, PyTorch, OpenCV, and ONNX Runtime. These are research directions, not a final trained model or established benchmark [S4, S5]. The baseline model, alternative configuration, input/output contract, dependencies, and numerical resource needs must be recorded before platform qualification. TensorRT belongs to the older Jetson alternative; it is not a Pi 5 acceptance dependency.

- Deliver dataset/split rationale, approved baseline and alternative artifacts, preprocessing and output contracts, model/version metadata, and precision/recall/F1/false-alert evaluation.
- Provide image/model trust-monitoring methods and support candidate/shadow evaluation under the existing SRS requirements.
- Benchmark on the selected Pi with Tomiwa; keep model accuracy evaluation distinct from network, buffering, or hardware reliability.

## 7 James Connolly backend and central controller

James owns the controller, registration/node-state model, APIs, messaging decision, ingestion, global adaptation policy, deployment/rollback orchestration, and audit coordination. With Tomiwa and Ethan he defines durable event/image ingestion, idempotent retry, incomplete upload state, and the receipt that permits local evidence completion. He separates source time, receive time, and fresh liveness.

- Deliver controller/API/message contracts, node registry and state tracking, policy and command services, deployment lifecycle, and ingestion/receipt behavior.
- Define a migration scenario with an input accessible to the receiving station; live USB-camera relocation is not implied by process reassignment.

## 8 Ethan McKissic dashboard and shared persistence

Ethan owns operator views, review workflows, configuration surfaces, central database schema, historical metrics, audit views, and representative-image persistence/retrieval. He coordinates with James on APIs and with Tomiwa on record/image identities and retention. Offline events retain source time and are reviewable only when their referenced image is complete.

The Early Status Report describes a preference for PostgreSQL with TimescaleDB, while older documents leave that decision open. Ethan and James shall reconcile the recorded configuration; optional Redis usage remains separate. This revision does not invent a completed database implementation [S5].

- Deliver station monitoring, smoke-review queue, model/configuration controls, history/audit views, central schema and migrations, and image lifecycle rules.
- Represent incomplete evidence explicitly and prevent late buffered data from making an offline station appear currently healthy.

## 9 Dylan Mcintee reliability and validation

Dylan owns the fault-injection program, repeatable inputs, automated/integration tests, experiment records, CI/observability coordination, and comparative evaluation. He tests physical/platform failures with Tomiwa, model conditions with Diego, ingestion/policy with James, and persistence/review with Ethan. Thermal and resource scenarios shall specify whether conditions are physically measured, induced by load, or simulated.

- Deliver fault matrix, experiment protocol, metrics definitions, scripts/configuration, comparative results, and acceptance evidence.
- Measure power/thermal/inference behavior and offline metadata-plus-image delivery within a declared load/capacity envelope; do not label planned procedures as results.

## 10 Responsibility and integration matrix

| Workstream | Primary owner | Support |
| --- | --- | --- |
| System architecture and interface coordination | Anthony Terry | All owners |
| Physical edge hardware and connection diagrams | Tomiwa Aluko | Anthony; Diego for resource constraints |
| Power cooling storage and camera selection | Tomiwa Aluko | Diego; Dylan for measurement |
| Edge agent camera adapters telemetry | Tomiwa Aluko | James; Diego |
| ML dataset training and model artifacts | Diego Mendoza | Tomiwa for runtime measurements |
| Image quality model disagreement and input change methods | Diego Mendoza | Dylan; Tomiwa integrates execution |
| Central policy messaging and ingestion | James Connolly | Anthony; Tomiwa |
| Central database snapshot storage and review availability | Ethan McKissic | James; Tomiwa supplies evidence |
| Local metadata image outbox and sync client | Tomiwa Aluko | James and Ethan define durable receipt |
| Model deployment coordination and rollback policy | James Connolly | Diego; Tomiwa executes edge changes |
| Dashboard and operator workflows | Ethan McKissic | James; Diego for result meaning |
| Fault injection comparative evaluation and validation | Dylan Mcintee | All owners |
| Shared release reproducibility and integration | Anthony Terry | Dylan; all owners |

## 11 Shared functional requirements

The original FR identifiers are retained. The system SRS provides detailed normative requirements and verification mappings. The following statements clarify the agreed hardware and evidence scope without removing the model lifecycle or trust-monitoring features.

| ID | Requirement | SRS mapping |
| --- | --- | --- |
| FR-01 | The system shall support at least three identified edge stations; the revision baseline requires three physical Pi 5 devices. | FR-1.1; HI-1.3 |
| FR-02 | Each edge station shall process live USB camera input or prerecorded footage using the common platform; initially one shared camera is required. | FR-2.1; HI-1.8 |
| FR-03 | Each edge station shall perform local smoke inference without continuous central connectivity. | FR-2.2 |
| FR-04 | Each station shall report temperature, memory, latency, throughput, connectivity, and device health with defined units and source times. | FR-3.1 to FR-3.4; DR-1.3 |
| FR-05 | Each station shall report model version, prediction, confidence, and relevant model-health information. | FR-2.3; FR-3.6 |
| FR-06 | The system shall evaluate image degradation including low light, fog, glare, blur, compression, camera movement, lens obstruction, and other significant visual changes using documented selected methods. | FR-3.5; FR-3.7 |
| FR-07 | The controller shall receive health and detection data from connected stations. | FR-1.3; FR-4.1 |
| FR-08 | Potential smoke shall create an event sufficient for operator review. | FR-4.1; DR-1.2 |
| FR-09 | A human operator shall be capable of reviewing detections before the research prototype treats them as human verified. | FR-4.3 |
| FR-10 | The dashboard shall show the representative frame, confidence, station, source time, model, and recent history, including recovered offline events. | FR-4.2; UI-1.2 |
| FR-11 | The controller shall support reducing processing frame rate under resource limitations. | FR-5.1 |
| FR-12 | The controller shall support reducing preprocessing resolution under resource limitations. | FR-5.2 |
| FR-13 | An edge station shall switch between at least two approved model configurations. | FR-2.4; FR-5.3 |
| FR-14 | The system shall demonstrate processing transfer/redirection in a documented failure/degradation scenario with a source accessible to the destination. | FR-5.4 |
| FR-15 | The system shall maintain identifiable model and deployment versions. | FR-6.1; SI-1.4 |
| FR-16 | A candidate model shall operate alongside the active model without controlling active alerts. | FR-6.2 |
| FR-17 | The system shall record and compare active/candidate outputs. | FR-6.3 |
| FR-18 | The system shall support limited or canary rollout of candidate models. | FR-6.5 |
| FR-19 | The system shall return to the known-good model when a candidate is unacceptable under the documented policy. | FR-6.6 |
| FR-20 | Healthy stations shall continue local processing during network loss while their local source remains available. | FR-7.1 |
| FR-21 | Detection records produced offline shall be stored locally with a representative image and retained telemetry under the capacity policy. | FR-7.2; FR-7.6 |
| FR-22 | Buffered records and images shall synchronize after reconnection with stable identities and source timestamps. | FR-7.3 to FR-7.5 |
| FR-23 | The system shall audit deployments, rollback, workload movement, failures, recovery, operator actions, and evidence-retention failures. | FR-8.1; FR-8.2 |
| FR-24 | Operators shall configure temperature, memory, latency, throughput, and manual-review limits. | FR-8.3 |

## 12 Reliability requirements

| ID | Requirement | SRS mapping |
| --- | --- | --- |
| RR-01 | Failure of one station shall not crash the central controller or healthy stations. | NFR-1.3 |
| RR-02 | Network loss shall not prevent local inference on a healthy station. | NFR-1.1 |
| RR-03 | Accepted buffered detections and images shall remain recoverable within the declared outage envelope. | NFR-1.2; FR-7.7 |
| RR-04 | The system shall detect loss of station contact using fresh liveness information. | FR-1.2; FR-1.3 |
| RR-05 | Recovery evidence shall show the action and its success or failure. | FR-5.5; NFR-2.4 |
| RR-06 | Model deployments shall be versioned. | FR-6.1; DR-1.4 |
| RR-07 | A known-good model shall remain available for rollback. | NFR-1.4 |
| RR-08 | Critical adaptation decisions shall be auditable. | NFR-5.2 |

## 13 Machine learning requirements

| ID | Requirement | SRS mapping |
| --- | --- | --- |
| ML-01 | At least one model shall detect wildfire smoke in fixed-view imagery/video. | FR-2.2; FR-4.1 |
| ML-02 | At least two model versions/configurations shall exist for comparison and switching. | FR-2.4 |
| ML-03 | Evaluation shall calculate precision, recall, F1, and false-alert rate with documented definitions. | FR-9.5 |
| ML-04 | Inference performance shall be measured on the selected physical edge hardware. | NFR-2.1; NFR-2.2 |
| ML-05 | Detection events shall retain model confidence with defined semantics. | FR-2.3; DR-1.2 |
| ML-06 | Active and candidate model results shall be comparable on corresponding inputs. | FR-6.2; FR-6.3 |
| ML-07 | Model performance shall be evaluated under degraded image conditions. | FR-9.2; FR-9.5 |

## 14 Experimental requirements

Compare a fixed deployment, simple temperature-threshold controller, and full EmberFlow under equivalent retained input and fault schedules. Define precision, recall, F1, false-alert rate, time to detection, input-change identification time, availability, recovery time, inference latency, buffered-alert delivery success, and rollback success. Specify denominators, observation windows, ground truth, and measurement limits. Camera capture rate and inference throughput are different measurements.

Separate live camera integration from detector accuracy claims. Recorded labeled footage supports reproducible detection evaluation. All hardware/model/software configurations, source clips, fault timing, target limits, and trial conditions shall accompany the results. Synthetic or staged imagery must be labeled rather than represented as a validated real-fire detection result.

## 15 Fault injection and evidence

Required scenarios include low light, fog, blur, compression, camera movement, network outage/recovery, node failure, thermal/resource load, and poor/failed candidate deployment. Research also considers glare and lens obstruction under FR-06; the selected evaluation protocol shall record coverage and limits. Add USB camera loss, application restart, interrupted image upload, missing durable receipts, delayed/stale telemetry, and storage-full behavior for the revised edge/evidence design.

Every run records setup, injected condition, expected response, accepted/rejected evidence counts, observations, recovery outcome, and artifact references. Zero missing accepted event/image pairs and zero duplicate event identities are required within the declared offline test envelope; operation beyond that envelope must follow and expose the documented policy.

## 16 Nonfunctional requirements

| ID | Requirement | SRS mapping |
| --- | --- | --- |
| NFR-01 | Major subsystems should use documented interfaces for independent development and testing. | NFR-3.1 |
| NFR-02 | Experiments should retain configurations, inputs, scripts, and relevant seeds for reproducibility. | NFR-6.1 |
| NFR-03 | Major components should emit structured logs and measurable metrics. | NFR-5.1 |
| NFR-04 | Subsystem documentation should cover setup, interfaces, configuration, and expected behavior. | NFR-3.4 |
| NFR-05 | Critical controller, buffering, deployment, adaptation, and synchronization behavior should have automated tests where practical. | NFR-3.3 |
| NFR-06 | Services that can reasonably be containerized should use Docker deployment definitions. | NFR-6.2 |
| NFR-07 | Each automatic adaptation should identify its trigger, action, and outcome. | NFR-5.2 |
| NFR-08 | Operators should retain appropriate review and override capability for the research prototype. | FR-4.3; UI-1.3; UI-1.4 |

## 17 Remaining development and evidence plan

| Gate | Evidence | Owners |
| --- | --- | --- |
| Before procurement | Hardware comparison, total budget, equipment inventory, model/runtime compatibility plan, and provisional BOM. | Tomiwa, Diego, Anthony |
| Before the midterm evidence freeze | Hardware diagram, interface table, named ownership, test profile draft, and a truthful account of completed versus planned work. | All owners |
| Before qualification | One Pi bring-up, USB video capture, power/thermal observations, model benchmark, and signed interface/test profiles. | Tomiwa and Diego; James supports integration |
| Before SD1 final evidence freeze | Component comparisons, available hardware/bench evidence, reproducible setup progress, schematics or connection documentation appropriate to this project, and remaining integration plan. | Tomiwa with Anthony |
| Early SD2 integration | Replicate three physical stations; connect central host; demonstrate detection, telemetry, commands, and offline record/image synchronization. | Tomiwa, James, Ethan, Diego |
| SD2 evaluation and final review | Complete recovery/model lifecycle/trust-monitoring tests and three-controller comparison; close traceability with actual evidence. | Dylan coordinates; all owners |

Replace elapsed generic month labels with actual remaining gates. The October 2 ECE archive lists November 6 midterm, November 9/10/12 meeting, November 13 revision, and December 3 final report/mini demo [S9]. These are archived ECE checkpoints that must be reconciled with the CS-led team's applicable calendar. No unconfirmed purchase or implementation completion date is implied. SD2 dates require the team's schedule.

## 18 Shared team obligations

- Participate in requirements/architecture/interface reviews, integration and code review, experiments, documentation, and final presentation/demonstration.
- Understand the complete data path and explain individual subsystem choices, interfaces, failure behavior, and evidence.
- Keep completed work, proposed design, open decisions, and measured results distinct.

## 19 Repository and configuration records

Retain versioned areas for edge, ML, controller, dashboard, data, testing, infrastructure, experiments, and documentation. Record hardware inventory and diagrams under documentation, schemas under shared interface records, model/version metadata with the ML/deployment artifacts, and experiment profiles with results. Exact file/module names remain implementation choices. Do not store project secrets in shared source history.

## 20 Definition of done and open decisions

| Gate | Acceptance | Verification |
| --- | --- | --- |
| AC-1 | Three station operation: Three physical Pi 5 stations register, process input, and report status over the wired network. Development simulation does not close this gate. | EDGE-TEST-02; EDGE-TEST-13 |
| AC-2 | End to end detection: Live webcam and replay inputs produce local results that reach central persistence and human review. | SYS-TEST-01 |
| AC-3 | Beyond uptime monitoring: Device health plus the required image/model trust signals are demonstrated. | EDGE-TEST-05; SYS-TEST-02 |
| AC-4 | Adaptive recovery: At least three distinct mechanisms from frame-rate reduction, resolution reduction, smaller-model switch, workload movement, and rollback are demonstrated. Every individual mandatory requirement still needs its own evidence. | SYS-TEST-03 |
| AC-5 | Offline continuity: Healthy local processing continues and all accepted metadata/images within the frozen outage envelope become reviewable after reconnection. | EDGE-TEST-17; EDGE-TEST-18 |
| AC-6 | Model lifecycle: Active/candidate comparison, operator feedback, limited rollout, and rollback pass their defined tests. | SYS-TEST-04 |
| AC-7 | Auditability: Trigger, action, actor, and outcome can be reconstructed for significant events. | SYS-TEST-07 |
| AC-8 | Controlled faults: Environmental, network, hardware/resource, and deployment faults can be repeated using recorded methods. | SYS-TEST-05 |
| AC-9 | Comparative evaluation: Fixed, simple threshold, and full EmberFlow results use comparable retained inputs and defined metrics. | SYS-TEST-05 |
| AC-10 | Research prototype boundary: Final materials preserve human verification and the research-prototype boundary. | SYS-TEST-09 |
| AC-11 | Platform handoff: A non-owner teammate reproduces a supported station and integrates an agreed algorithm/model adapter using versioned instructions. | EDGE-TEST-20 |
| AC-12 | Hardware evidence: Physical diagram, BOM, connection record, power/thermal/performance observations, and frozen targets match the assembled hardware. | EDGE-TEST-14; EDGE-TEST-15; EDGE-TEST-21 |

The shared completion gate requires all mandatory SRS requirements and evidence, not merely the summary gates. Each owner supplies actual results for their responsibilities. The current documents do not establish that any listed hardware or software acceptance test has passed.

### OD 1 Pi variants and accessory configuration

Owner: Tomiwa with Diego and Anthony. Closure gate: Before procurement. Record RAM/storage/cooling/supply/camera comparison and available equipment. Pi 5 board family is the revision baseline.

### OD 2 MQTT or NATS and image transfer

Owner: James with Tomiwa and Anthony. Closure gate: Before integration contract freeze. Choose messaging, endpoints, acknowledgment semantics, transport controls, and durable image upload protocol.

### OD 3 Central persistence configuration

Owner: Ethan with James. Closure gate: Before durable-ingestion test. Reconcile the status report statement favoring PostgreSQL with TimescaleDB with older open-decision language; document the versioned configuration. Redis remains optional.

### OD 4 Baseline and alternative models

Owner: Diego with Tomiwa. Closure gate: Before platform performance qualification. Select model artifacts, runtime, dependencies, and preprocessing; demonstrate model compatibility on one Pi.

### OD 5 Image quality and input change algorithms

Owner: Diego with Dylan. Closure gate: Before trust-monitoring tests. Define methods and evaluation inputs; preserve existing system requirements pending explicit team scope changes.

### OD 6 Numerical acceptance profile

Owner: Tomiwa, Diego, James, Dylan. Closure gate: Before qualification testing. Freeze capture modes, throughput/latency limits, heartbeat and freshness intervals, recovery bounds, thermal/power conditions, and test duration.

### OD 7 Workload movement scenario

Owner: James with Tomiwa and Dylan. Closure gate: Before migration test. Define a source accessible to the receiving node. Shared recorded footage is a recommended first scenario, not a promise of live USB-camera failover.

### OD 8 Budget and sourcing

Owner: Anthony and team with Tomiwa. Closure gate: Before any purchase. Set total cap, funding, itemized quotations, taxes/shipping allowance, inventory, and procurement lead time. No cost is asserted without a quote.

### OD 9 Offline capacity and image lifecycle

Owner: Tomiwa, James, Ethan. Closure gate: Before outage acceptance test. Set retention, image format/size cap, quotas, outage workload envelope, retry/ack protocol, and full-buffer policy.

### OD 10 Central host and wired network configuration

Owner: James, Ethan, Anthony, Tomiwa. Closure gate: Before three-station integration. Identify existing host and equipment; record OS, adapters, addresses, broker/API location, ports, and service startup.

## Source references

[S1] EmberFlow Senior Design SRS version 1.0. C:\Users\gokug\Downloads\EmberFlow_Senior_Design_SRS (1).pdf

[S2] EmberFlow Role 2 Subsystem Specification version 1.0. C:\Users\gokug\Downloads\EmberFlow_Role2_Edge_Computing_Subsystem_Specification.pdf

[S3] EmberFlow Roles and Requirements Specification version 1.0. C:\Users\gokug\Downloads\EmberFlow_Roles_and_Requirements_Specification (1).pdf

[S4] Design Proposal and Team Contract dated September 22 2026, reviewed October 22. https://docs.google.com/document/d/1YqJpT0JMOyfTeAuKt24NWQ1deJEBbWxRE7mwEsNbeQE/edit?tab=t.0

[S5] Early Status Report reviewed October 22 2026, ML status snapshot October 6. https://docs.google.com/document/d/1q3VX7D0t_VJfdb-lvgFS4zNtR2bU10tzd3vvGd2L2iY/edit?tab=t.0

[S6] Tomiwa approved revision decisions and professor feedback, October 22 2026. Current project discussion; approval is for this document revision, not a claim of team-wide ratification or completed implementation.

[S7] Raspberry Pi computer hardware documentation, checked October 22 2026. https://www.raspberrypi.com/documentation/computers/raspberry-pi.html

[S8] Raspberry Pi camera software and USB webcam documentation, checked October 22 2026. https://www.raspberrypi.com/documentation/computers/camera_software.html#use-a-usb-webcam

[S9] Senior Design course dates captured October 2 2026. TundeBrain/Reference/Courses/Senior Design I - Fall 2026/SD1 - Deadlines and Assignment Access.md; historical course snapshot, not live confirmation of CS-led project deadlines.
