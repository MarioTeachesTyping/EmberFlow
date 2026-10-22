# EmberFlow Edge Computing and Embedded Systems Specification

Tomiwa Aluko individual subsystem and teammate platform

EF-R2-001 | Revision 1.1 | October 22 2026 | Review draft

I am responsible for the physical edge-computing platform on which EmberFlow receives camera footage, runs local smoke inference, measures device condition, and preserves review evidence during a network outage. This specification identifies my hardware work, my software interfaces, and the evidence I will provide for that contribution.

Revision 1.1 implements the hardware-focused document revision approved by Tomiwa on October 22, 2026. It is a review draft for faculty and team reconciliation. Requirements describe intended behavior; no procurement, trained model, hardware benchmark, or implementation result is asserted by this document.

### Document control

| Revision | Basis |
| --- | --- |
| 1.0 | Original attached specification; retained as the source baseline. |
| 1.1 | Named owners; Pi 5 indoor platform; USB camera and wired Ethernet; existing central host; offline image evidence; physical diagrams; interface and verification updates. |

Shall identifies an acceptance obligation; should identifies a recommendation; may identifies an option. A chosen architecture is distinguished from an unselected part or proposed implementation. The professor clarification that no custom PCB is required was reported by Tomiwa [S6]; it does not waive unrelated ECE coursework or writing obligations.

## 1 Subsystem purpose and team ownership

| Role | Member | Ownership |
| --- | --- | --- |
| R2 | Tomiwa Aluko | Edge hardware and embedded platform |
| R1 | Anthony Terry | Architecture and system integration |
| R3 | Diego Mendoza | Machine learning and computer vision |
| R4 | James Connolly | Backend and central controller |
| R5 | Ethan McKissic | Dashboard and shared persistence |
| R6 | Dylan Mcintee | Reliability and validation |

Tomiwa is the only Computer Engineering member; the other five members are Computer Science students. James also appears as Gabe or Gabriel in source documents and Jira. This revision uses James Connolly consistently for formal ownership. Ownership assigns accountability without excluding shared integration, testing, and documentation.

I will select and integrate the station hardware, configure a repeatable Linux environment, connect the USB camera, provide video frames to Diego's model adapter, measure device and inference performance, execute approved controller commands, and implement local evidence storage and synchronization. Diego owns model development and image/model monitoring algorithms. James owns central policy and ingestion. Ethan owns central persistence and operator views. Anthony coordinates architecture and integration. Dylan coordinates reliability experiments and validation.

The platform deliverable is complete only when another teammate can deploy an agreed component using its documented interfaces and reproduce the supported station setup. Running a model once is not sufficient evidence of hardware integration, reliability, or reproducibility.

## 2 Confirmed scope and status

| Area | Revision baseline |
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

These are the approved document-planning choices, not a statement that hardware is available or that every team decision has been ratified. No custom PCB, extra microcontroller, outdoor enclosure, field battery, or cellular link is introduced. Existing system requirements for candidate models, trust monitoring, workload movement, and controlled rollback remain in scope unless the team formally changes them.

## 3 Physical hardware architecture

![Figure 1. One physical station and its external connections. Local storage medium and cooling details are proposed pending component selection.](diagrams/station_hardware.png)

The board exposes USB, Ethernet, USB C power, and removable storage interfaces described by Raspberry Pi [S7]. This design uses USB for the webcam and Ethernet for inter-node communication. USB camera capture is documented by Raspberry Pi [S8], but the selected device, video modes, and recovery behavior must be tested on the chosen OS. GPIO, CSI, and custom peripheral buses are not part of the chosen camera connection.

| ID | Requirement |
| --- | --- |
| R2-HW-01 | I shall deliver and document three physical Raspberry Pi 5 stations for final demonstration. |
| R2-HW-02 | I shall define and verify a common hardware/software platform, including the shared USB webcam on each station in turn. |
| R2-HW-03 | I shall document supply and cable ratings, peripheral demand, and observed power-status behavior under the recorded load profile. |
| R2-HW-04 | I shall select compatible cooling and document mounting, ambient/test conditions, temperature behavior, and any throttling observed under sustained inference. |
| R2-HW-05 | I shall size and document boot/data storage for the OS, model versions, accepted offline events/images, telemetry, and logs, including quotas and free-space reserve. |
| R2-HW-06 | I shall document a wired Ethernet topology connecting all three stations and the existing central computer. |
| R2-HW-07 | I shall maintain a physical hardware diagram, connection record, BOM, and individual station inventory consistent with the actual assemblies. |
| R2-HW-08 | I shall document the indoor mounting and cable arrangement so ventilation, camera framing, and storage/connectors remain usable during demonstration. |
| R2-HW-09 | I shall report measured hardware/model behavior against a versioned qualification profile frozen before acceptance testing. |
| R2-HW-10 | I shall record camera loss separately from network loss; continued inference after network loss requires a still-available local source. |

![Figure 2. Three physical stations use wired Ethernet to an existing central computer. Each station has a compatible supply, storage, and cooling.](diagrams/system_deployment.png)

## 4 Component selection and bill of materials

| Item | Quantity | Selection evidence |
| --- | --- | --- |
| Raspberry Pi 5 | 3 | RAM variant pending measured model and concurrent-service memory needs. |
| Compatible USB C supply and cable | 3 sets | Select for Pi plus attached USB camera and cooling load; document ratings and test power status under load. |
| Local boot and data storage | 3 | microSD is the proposed initial medium; capacity, endurance, free-space reserve, and alternatives remain comparison decisions. |
| Cooling assembly | 3 | Choose compatible cooling and mounting after sustained-load measurements; fan connection depends on selected assembly. |
| Compatible USB webcam | 1 | Select and test Linux support, video modes, timestamps, disconnect recovery, USB bandwidth, and peripheral power demand. |
| Ethernet switch or router | 1 | At least four usable endpoint ports for three Pis and the central host; confirm available equipment and addressing service. |
| Ethernet patch cable | 4 | One for each Pi and one for the central host. Add any required uplink cable separately. |
| Existing laptop or desktop | 1 existing | Confirm operating environment, memory, storage, and Ethernet access with central-service owners. |
| Ethernet adapter | 0 or 1 | Only if the selected central computer lacks a suitable Ethernet interface. |
| Mounting and cable management | As needed | Stable indoor mounting, ventilation clearance, protected storage access, and cable strain relief. |

No prices or purchased quantities are claimed. The cost worksheet shall record supplier, quotation date, unit cost, shipping/tax, extended cost, available equipment, lead time, and funding source. The total includes three supplies, three storage devices, three cooling solutions, one webcam, four endpoint cables, network equipment, and any central-host Ethernet adapter. Team budget approval precedes procurement.

Compare Pi RAM variants against the measured model working set and concurrent capture, telemetry, buffering, and candidate-runtime load. Compare storage options against write endurance, sustained writes, capacity, recovery, power, and interface complexity. Compare webcams by demonstrated Linux support, field of view, focus, video modes, exposure behavior, bandwidth, and power. A larger sensor resolution or more RAM alone is not evidence that the workload meets its targets.

## 5 Physical connections and network communications

| ID | Endpoints | Interface | Design record |
| --- | --- | --- | --- |
| PWR1 | Supply to each Pi | USB C input; power into Pi | Record supply/cable ratings and combined board, webcam, storage, and cooling demand. Verify power-status indications under representative load. No custom power circuit. |
| CAM1 | USB webcam to active station | USB data into Pi; peripheral power from Pi | Document USB version, device identity, driver, video mode, frame format, cable, power demand, and recovery. Only one webcam is required initially. |
| STO1 | Pi to local storage | Bidirectional local storage interface | Proposed microSD; final media/interface pending comparison. Retain OS, model versions, event metadata, snapshots, telemetry, and logs within documented quotas. |
| NET1 | Each Pi to local network | Bidirectional Ethernet through RJ45 | Three station links. Record addresses, negotiated link, routes, application endpoints, retries, and disconnect behavior. Link presence and controller reachability are separate states. |
| NET2 | Central host to local network | Bidirectional Ethernet | Existing host uses native Ethernet or compatible adapter. Router addressing or switch-only static addressing is a documented integration decision. |
| COOL1 | Cooling to each Pi | Thermal path; electrical connection if active | Record mounting, airflow clearance, power/control connection, and observed thermal behavior for the selected assembly. Do not assume a fan connector before selecting the assembly. |

Each endpoint requires a network address and documented service destinations. A router can supply addressing, while a switch-only setup needs an explicit addressing plan. James and Anthony approve the service/address configuration with me. The network equipment and central host retain their own power arrangements. Ethernet is the data link; this baseline does not assume power over Ethernet.

For every selected component, record manufacturer/model, connector/cable, signal or power direction, relevant electrical rating, driver/OS support, and observed fault behavior. Do not copy an unverified pinout into the design. No custom GPIO wiring is required by this revision.

## 6 Edge operating environment

Use a reproducible Linux environment compatible with the chosen Pi, webcam, and ML runtime. A current Raspberry Pi OS 64-bit image is a proposed starting point, not a frozen OS/version decision. Record image/version, installation steps, users/permissions, USB device identity, network configuration, service manager, containers where practical, model artifacts, and recovery commands. Keep node identity and credentials outside the reusable image where appropriate.

| ID | Requirement |
| --- | --- |
| R2-FR-1.1 | The edge software shall automatically initialize after the edge device boots. |
| R2-FR-1.2 | The edge software shall load node-specific configuration. |
| R2-FR-1.3 | Each edge station shall have a persistent unique identifier. |
| R2-FR-1.4 | The node shall determine whether required services are available before entering operational state. |
| R2-FR-2.1 | Each edge node shall register itself with the EmberFlow controller. |
| R2-FR-2.2 | Registration shall include at minimum the Node ID, hostname, device type, software version, model version, and current health status. |
| R2-FR-2.3 | The node shall retry registration following temporary registration failure. |
| R2-FR-3.1 | Every node shall periodically publish a heartbeat. |
| R2-FR-3.2 | The heartbeat shall allow the controller to determine whether the node remains reachable. |
| R2-FR-3.3 | Heartbeat frequency shall be configurable. |
| R2-FR-17.1 | Edge services that can reasonably be containerized shall be deployable through Docker. |
| R2-FR-17.2 | Deployment configuration shall be version controlled. |
| R2-FR-17.3 | A new team member shall be able to reproduce the edge environment using project documentation. |

## 7 Camera and video pipeline

The input adapter shall select either the USB webcam or an identified local video file. Attach a source/frame ID and source timestamp before inference. Record capture resolution/rate and decoded pixel layout separately from preprocessing/model input shape and processing rate. Dropped or intentionally skipped frames shall be distinguishable from camera failure.

Camera absence produces an explicit input failure/degraded state and a recoverable error. A network outage does not remove the local camera or local replay file. Preprocessing changes must remain compatible with the selected model; controller resolution commands cannot silently violate its tensor shape or normalization contract.

| ID | Requirement |
| --- | --- |
| R2-FR-4.1 | The edge system shall support prerecorded video files. |
| R2-FR-4.2 | The common edge platform shall support the selected USB webcam, verified on each station in turn; one webcam is required initially. |
| R2-FR-4.3 | The video subsystem shall produce individual frames suitable for ML processing. |
| R2-FR-4.4 | Frame rate shall be configurable. |
| R2-FR-4.5 | Video resolution shall be configurable. |
| R2-FR-4.6 | The subsystem shall expose current video-source status. |

## 8 Teammate platform and ML interface

![Figure 3. Logical edge data flow and durable review-evidence delivery. This complements the physical diagrams and does not represent extra hardware.](diagrams/edge_evidence_flow.png)

Diego supplies the validated model artifacts, training/evaluation methodology, input requirements, preprocessing definition, output interpretation, and image/model monitoring algorithms. I provide capture adapters, the runtime integration environment, measured hardware constraints, scheduling, result envelopes, and edge execution/recovery mechanisms. Where preprocessing is implemented in the edge pipeline, Diego specifies and validates its mathematical meaning; I implement and test the agreed interface.

| Contract part | Required agreement |
| --- | --- |
| Frames | Source/frame IDs; source timestamp and clock quality; width/height; pixel format and channel order; data type; ownership/lifetime of the frame buffer. |
| Preprocessing | Resize/crop/letterbox behavior, normalization, input tensor layout, supported shapes, and one accountable implementation location. |
| Artifact | Model/version and integrity identifier; runtime and dependency versions; supported precision; resource expectations; startup and load errors. |
| Results | Prediction/detection semantics, confidence meaning, model version, inference latency boundary, source/frame association, and error schema. |
| Representative image | The frame associated with the event, encoding/size policy, immutable image identity and integrity value, and retention state. |
| Monitoring modules | Versioned image-quality/change/disagreement outputs, sampling settings, error states, and integration ownership. |

| ID | Requirement |
| --- | --- |
| R2-FR-5.1 | The edge node shall load an approved smoke-detection model. |
| R2-FR-5.2 | The node shall support the team-selected runtime verified on Raspberry Pi 5. Python, PyTorch, OpenCV, and ONNX Runtime remain candidates; historical Jetson/TensorRT alternatives are not acceptance obligations for this Pi baseline. |
| R2-FR-5.3 | The system shall pass processed video frames to the ML runtime. |
| R2-FR-5.4 | The system shall capture inference results. |
| R2-FR-5.5 | Inference records shall preserve source timestamp, station/frame identity, model version, prediction/detection status, confidence, and measured latency under the agreed schema. |
| R2-FR-5.6 | The runtime shall measure inference latency. |

| ID | Requirement |
| --- | --- |
| R2-PLT-01 | I shall provide versioned setup, configuration, model-adapter, deployment, and troubleshooting documentation for supported Pi hardware. |
| R2-PLT-02 | I shall agree and version the frame/model/result contract with Diego and the event/message contract with James and Anthony. |
| R2-PLT-03 | I shall provide a small deterministic input/output fixture for teammate integration before model accuracy is used as a platform test. |
| R2-PLT-04 | A teammate other than me shall reproduce a supported station and integrate the agreed fixture and approved model adapter using the documented process; deviations shall be recorded. |
| R2-PLT-05 | I shall benchmark the selected baseline model on one physical Pi with Diego before freezing remaining station variants and performance commitments. |

The fixture demonstrates interface compatibility only; it does not establish smoke-detection accuracy. The production model remains a joint integration dependency. FIgLib and lightweight YOLO-family architectures are candidates from the reviewed proposal; a specific model/runtime is not yet established [S4, S5].

### Proposed integration example

A teammate selects an identified replay frame, supplies an adapter that accepts the frozen frame format, and returns a deterministic fixture result with model identity and latency. The platform wraps that result with station/frame/time identity and links the same source frame as the event image. The test checks schema and association before substituting Diego's approved model artifact. Actual adapter code, exact field names, and tensor shapes are deliverables to be frozen jointly, not claimed as already implemented here.

## 9 Telemetry and controller integration

Publish CPU, memory, available temperature, inference latency, processing throughput, camera state, free storage/backlog, model version, and controller connectivity with defined units and source times. The controller determines policy thresholds and station reachability; the edge reports measurements and executes valid requests. Keep source time, receive time, station session, and sequence distinct so replay does not refresh current health. Use monotonic durations for latency and report clock uncertainty after boot/outage until time is established.

| ID | Requirement |
| --- | --- |
| R2-FR-6.1 | CPU utilization shall be measured. |
| R2-FR-6.2 | Memory consumption shall be measured. |
| R2-FR-6.3 | Available hardware temperature sensors shall be monitored. |
| R2-FR-6.4 | The subsystem shall measure inference latency. |
| R2-FR-6.5 | Inference throughput shall be measured. |
| R2-FR-6.6 | The subsystem shall monitor connectivity to the central controller. |
| R2-FR-6.7 | The subsystem shall monitor free storage and evidence backlog because outage retention depends on capacity. |
| R2-FR-7.1 | The Edge Agent shall maintain a local health state. |
| R2-FR-7.2 | The health subsystem shall detect excessive resource consumption based on configurable thresholds. |
| R2-FR-7.3 | Health information shall be reported to the controller. |
| R2-FR-7.4 | The node shall log transitions between health states. |
| R2-FR-8.1 | The edge node shall receive controller commands. |
| R2-FR-8.2 | Commands shall contain a unique command ID. |
| R2-FR-8.3 | The Edge Agent shall acknowledge received commands. |
| R2-FR-8.4 | The Edge Agent shall report whether execution succeeded, failed, or was rejected. |
| R2-FR-8.5 | Failed commands shall generate structured error information. |

| ID | Requirement |
| --- | --- |
| R2-IF-01 | I shall document controller endpoints, selected messaging/transfer protocol, topics/routes, schema version, authentication/access mechanism, and retry rules jointly with the central owners. |
| R2-IF-02 | Commands shall be validated for schema, station target, supported operation, parameter limits, expiry/freshness, and duplicate identity before a state change. |
| R2-IF-03 | Command responses shall distinguish receipt from terminal success, failure, or rejection and correlate to the command ID. |
| R2-IF-04 | Telemetry shall carry station/session/sequence and source-time information; delayed replay shall remain historical rather than reset liveness. |
| R2-IF-05 | Capture rate, processing throughput, inference latency, connection state, and camera health shall have separate defined measurement meanings. |

Draft command vocabulary: SET_FRAME_RATE, SET_RESOLUTION, SWITCH_MODEL, PAUSE_PROCESSING, RESUME_PROCESSING, RESTART_WORKER, REQUEST_STATUS, START_BUFFER_SYNC, and PREPARE_MIGRATION. Names and parameter schemas are proposed interface details; freeze them with James before integration. Invalid commands produce explicit rejection rather than an unreported state change.

## 10 Offline evidence storage and synchronization

Treat each accepted detection as metadata plus a representative image with stable event/image identities. Persist the association before considering the event accepted. A proposed implementation is a SQLite outbox plus image files written to durable local storage with integrity metadata and recoverable commit ordering; the final mechanism remains an implementation decision. Telemetry and structured logs use separate bounded policies.

| ID | Requirement |
| --- | --- |
| R2-FR-13.1 | Loss of controller connection shall not terminate local video processing. |
| R2-FR-13.2 | Loss of network connectivity shall not terminate local inference. |
| R2-FR-13.3 | The edge node shall detect loss of controller connectivity. |
| R2-FR-13.4 | The node shall enter an appropriate offline/degraded state. |
| R2-FR-14.1 | Detection events awaiting delivery shall be stored persistently with one representative image per event, together with retained telemetry under the capacity policy. |
| R2-FR-14.2 | Buffered events shall preserve event ID, station/session/frame identity, source timestamp, model version, prediction/confidence, image reference and integrity metadata, and synchronization state. |
| R2-FR-14.3 | Accepted buffered metadata and representative images shall survive application restart with recoverable association and pending/completed state. |
| R2-FR-15.1 | The node shall detect restoration of controller connectivity. |
| R2-FR-15.2 | The Edge Agent shall begin synchronization of buffered records. |
| R2-FR-15.3 | Retries shall reuse stable event and image identities. Duplicate transmission is permitted after a missing durable receipt; the central path shall converge without duplicate event identities. |
| R2-FR-15.4 | An event shall be marked complete only after a durable central receipt confirms its metadata and complete representative image. Local retention or deletion after completion shall follow the documented policy. |

| ID | Requirement |
| --- | --- |
| R2-FR-14.4 | An accepted event shall have recoverable metadata/image association; incomplete image writes or missing image files shall be detected and reported. |
| R2-FR-14.5 | The buffer shall enforce documented quotas, free-space reserve, retention, and explicit full-buffer admission/eviction behavior without silently marking lost evidence as delivered. |
| R2-FR-14.6 | The station shall report backlog count/bytes, capacity state, retention failures, and accepted versus rejected evidence counts sufficient for reconciliation. |
| R2-FR-15.5 | A broker receipt or metadata-only response shall not cause deletion of an unsynchronized representative image. |
| R2-FR-15.6 | Interrupted uploads and missing receipts shall be retried using stable identities and an integrity/length check until complete or explicitly failed under the retention policy. |
| R2-FR-15.7 | Offline qualification shall account for every accepted event and image within a declared event-rate, snapshot-size, telemetry, outage-duration, and storage-capacity envelope. |

Estimate required usable buffer from maximum accepted event rate times outage duration times per-event metadata-plus-image bytes, then add telemetry, logs, staging/retry overhead, and reserve. Include retained model versions and OS usage separately. Measure encoded image sizes and event grouping behavior; do not size from raw video rate or assume unlimited retention. Freeze image size/encoding and full-buffer policy with James and Ethan before acceptance testing.

Central ingestion may receive metadata and images separately, but it must expose incomplete state until both are durable and retrievable together. Ethan owns shared storage and review availability; James owns ingestion/receipt semantics; I retain pending evidence and retry state. Once a complete receipt arrives, local deletion follows the agreed retention policy. Keeping one image per event does not require continuous video recording.

## 11 Adaptation and recovery

I implement edge mechanisms; James owns global policy. Support runtime processing-rate and preprocessing-resolution changes, approved model selection/rollback, worker start/stop, capacity reporting, and configured recovery. Treat connectivity and compute/input health as separate state dimensions so an offline station can remain locally functional. Log state transitions and outcomes with model and configuration identity.

| ID | Requirement |
| --- | --- |
| R2-FR-9.1 | The Edge Agent shall allow the processing frame rate to change while the system is running. |
| R2-FR-10.1 | Video preprocessing resolution shall be dynamically configurable. |
| R2-FR-10.2 | Changing resolution shall not crash the inference pipeline. |
| R2-FR-11.1 | At least two approved model versions shall be deployable to a node. |
| R2-FR-11.2 | The Edge Agent shall expose the currently active model version. |
| R2-FR-11.3 | The controller shall be capable of requesting model changes. |
| R2-FR-11.4 | The Edge Agent shall validate that a requested model artifact is available and loadable. |
| R2-FR-11.5 | The Edge Agent shall report model-switch success or failure. |
| R2-FR-12.1 | The previous known-good model shall remain available and restorable during candidate deployment, consistent with system requirement NFR-1.4. |
| R2-FR-12.2 | The edge system shall support returning to the previous model version. |
| R2-FR-16.1 | The Edge Agent shall expose whether it can accept additional workload. |
| R2-FR-16.2 | The edge node shall support starting and stopping designated processing workers. |
| R2-FR-16.3 | Workload transitions shall be logged. |
| R2-FR-18.1 | The system should detect unexpected termination of critical edge services. |
| R2-FR-18.2 | Critical edge services should automatically restart where appropriate. |
| R2-FR-18.3 | Restart events shall be logged. |

| ID | Requirement |
| --- | --- |
| R2-LOG-01 | Structured edge logs shall cover startup/shutdown, registration, network loss/restoration, inference errors, model load/switch/rollback, configuration and health changes, commands and outcomes, buffering/synchronization, storage/retention failure, worker restart, and processing failure. |

Workload movement requires an input available at the destination. A shared recorded clip is the recommended first test scenario pending OD-7. A USB camera remains physically attached to its station; live failover would require a separately designed source-sharing path. Do not claim that restarting a worker on another Pi automatically transfers the camera feed.

## 12 Verification and acceptance

| ID | Requirement |
| --- | --- |
| R2-NFR-1.1 | Reliability: The edge subsystem shall continue local inference following temporary controller/network loss. |
| R2-NFR-1.2 | Recoverability: The Edge Agent shall be capable of recovering from supported transient failures without requiring device reimaging. |
| R2-NFR-2.1 | Modularity: Video capture, telemetry, inference, buffering, communication, and health monitoring should be separated into logical modules. |
| R2-NFR-2.2 | Configurability: System thresholds and operational parameters should not be unnecessarily hard-coded. |
| R2-NFR-2.3 | Maintainability: Code shall use appropriate type hints where practical, documentation, clear naming, error handling, and configuration documentation. |
| R2-NFR-3.1 | Portability: common functionality should be isolated from device-specific code to ease reuse. Raspberry Pi 5 is the required hardware baseline; Jetson support is not required by this revision. |
| R2-NFR-4.1 | Observability: The subsystem shall provide sufficient telemetry and logs to determine why an edge node entered a degraded state. |
| R2-NFR-5.1 | Reproducibility: Another team member shall be able to configure a replacement device using documented procedures. |

Test, demonstration, inspection, and analysis are verification methods. Freeze the target profile before qualification. Before that point, bring-up and benchmarking produce characterization evidence only. Existing illustrative values such as 10 FPS, 720p, or a five-second heartbeat are not acceptance targets unless adopted in the recorded profile.

| Profile area | Fields to freeze | Owner |
| --- | --- | --- |
| Input and inference | Capture width/height, capture FPS, processing FPS, model input shape, model version, precision, runtime/version, latency statistic and bound | Diego and Tomiwa |
| Power and thermal | Supply/cable ratings, ambient conditions, peak load, temperature criterion, power-status criterion, cooling configuration, sustained-test duration | Tomiwa |
| Liveness and recovery | Heartbeat cadence, stale timeout, service-restart bound, registration/retry bounds, camera recovery bound | Tomiwa and James |
| Offline evidence | Outage duration, maximum accepted event rate, snapshot size, telemetry/log rate, usable buffer quota and reserve, overflow policy, sync completion bound | Tomiwa, James, Ethan |
| Repeatability | Dataset/clip identity and split, trial count, fault schedule, node hardware/software baseline, central-host configuration | Dylan with all owners |

### EDGE TEST 01 Boot and readiness

Cold boot with recorded station configuration. Verify automatic startup, persistent identity, dependency checks, and READY or explicit degraded state; measure boot time against the frozen profile.

### EDGE TEST 02 Registration and heartbeat

Connect three physical Pis. Verify three distinct registrations and configurable heartbeats. Stop one agent and observe timeout without treating buffered telemetry as live contact.

### EDGE TEST 03 Recorded video

Replay an identified local clip. Verify decoded frames, frame/source IDs, controllable processing rate and resolution, and clear source status.

### EDGE TEST 04 Model integration

Load the approved artifact and process identified frames. Verify schema, confidence semantics, model version, prediction, error reporting, and latency boundary; Diego checks model interpretation.

### EDGE TEST 05 Telemetry

Compare readings with device-level observations under idle and load conditions. Verify units, sample times, CPU/memory/temperature, latency, processing throughput, network, camera, and available-storage state.

### EDGE TEST 06 Disconnected inference

Disconnect the station Ethernet link while its USB camera or local file remains available. Verify continued local capture and inference, with explicit disconnected state and no dependence on controller access.

### EDGE TEST 07 Persistent buffer

Generate identifiable events offline and restart the application. Verify retained metadata, representative images, pending state, original identifiers, and documented restart behavior.

### EDGE TEST 08 Reconnection

Restore connectivity after the declared outage. Verify backlog upload, retained source times, central persistence, and complete event/image associations within the frozen synchronization bound.

### EDGE TEST 09 Processing rate command

Issue a valid lower processing-rate command during inference. Verify acknowledgment, measured new rate, continued operation, command ID, and outcome. Capture FPS may remain unchanged.

### EDGE TEST 10 Resolution command

Change preprocessing resolution to a supported model input configuration. Verify no crash, contract-compatible tensor, preserved evidence-frame association, and logged outcome.

### EDGE TEST 11 Model switch

Switch between two approved model configurations. Verify artifact/dependency checks, active version, command outcome, and an explicit failure result for an unloadable candidate.

### EDGE TEST 12 Worker recovery

Terminate an inference worker. Verify bounded configured restart, retained evidence, restored service or explicit failed state, and structured restart history without a full reimage.

### EDGE TEST 13 Shared USB camera

Move the single selected webcam between the three stations, powering down if required by equipment procedure. Verify capture and equivalent configuration on each; test camera absence/reconnect separately from network loss.

### EDGE TEST 14 Power and physical assembly

Inspect all supply/cable/storage/cooling connections. Under the recorded maximum test load, verify chosen power-status and thermal criteria, mounting, ventilation, and configuration inventory. Record instruments and measurement limitations.

### EDGE TEST 15 Sustained load and performance

Freeze the model/input/environment/test duration and target profile first. Measure latency distribution, processing FPS, memory, temperature, throttling/power status, and disk use through sustained operation; compare with the predeclared limits.

### EDGE TEST 16 Wired topology and host

Verify three station Ethernet links and the existing central host link, documented addresses/routes, service endpoints, restart procedures, and separation of link state from service reachability.

### EDGE TEST 17 Offline review evidence

Within the declared capacity envelope, create a counted set of accepted detections with identifiable snapshots. Disconnect/restart/reconnect as specified. Reconcile every accepted event and image centrally, with zero missing accepted records/images and zero duplicate event identities; open images in operator review.

### EDGE TEST 18 Retry and partial upload

Interrupt image upload and discard a central acknowledgment in controlled tests. Retry unchanged event/image IDs. Verify incomplete state remains visible, local evidence is retained until durable completion, and central retries converge to one complete event.

### EDGE TEST 19 Known good rollback

Deploy a failing or rejected candidate and restore the retained version. Verify loadability, restored active identity, continued evidence association, and controller audit outcome.

### EDGE TEST 20 Teammate handoff

A teammate other than Tomiwa follows versioned instructions on supported hardware, installs an agreed fixture then the approved model adapter, and produces correctly structured frames/results without undocumented owner-only steps. Record deviations.

### EDGE TEST 21 Design inventory

Inspect physical diagram, BOM, supply and peripheral ratings, per-node configuration, interface record, comparison rationale, and no-PCB scope. Match the records to the assembled devices.

### EDGE TEST 22 Workload movement

Use the frozen migration scenario and an input available to the receiving node. Verify capacity report, assignment, worker start/stop, result continuity definition, and audit outcome; do not claim physical USB-camera relocation.

### EDGE TEST 23 Contract and command validation

Review versioned schemas; exercise supported commands, invalid parameters, stale/duplicate commands, and response correlation. Verify unsupported changes are rejected and image/transport receipt semantics are distinguishable.

### EDGE TEST 24 Time and state freshness

Replay delayed telemetry and events after reconnect. Verify historical placement by source time, session/sequence handling, clock uncertainty reporting, and current liveness from fresh contact rather than replay arrival.

### EDGE TEST 25 Capacity boundary

Use a bounded test dataset to approach and exceed the configured storage quota. Verify reserve, backlog visibility, declared admission/retention behavior, explicit failure counts, and reconciliation of accepted versus rejected evidence.

### Requirement verification coverage

| Requirement | Verification procedure |
| --- | --- |
| R2-FR-1.1 | EDGE-TEST-01 |
| R2-FR-1.2 | EDGE-TEST-01 |
| R2-FR-1.3 | EDGE-TEST-01 |
| R2-FR-1.4 | EDGE-TEST-01 |
| R2-FR-2.1 | EDGE-TEST-02 |
| R2-FR-2.2 | EDGE-TEST-02 |
| R2-FR-2.3 | EDGE-TEST-02 |
| R2-FR-3.1 | EDGE-TEST-02 |
| R2-FR-3.2 | EDGE-TEST-02 |
| R2-FR-3.3 | EDGE-TEST-02 |
| R2-FR-4.1 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-4.2 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-4.3 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-4.4 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-4.5 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-4.6 | EDGE-TEST-03; EDGE-TEST-13 |
| R2-FR-5.1 | EDGE-TEST-04 |
| R2-FR-5.2 | EDGE-TEST-04 |
| R2-FR-5.3 | EDGE-TEST-04 |
| R2-FR-5.4 | EDGE-TEST-04 |
| R2-FR-5.5 | EDGE-TEST-04 |
| R2-FR-5.6 | EDGE-TEST-04 |
| R2-FR-6.1 | EDGE-TEST-05 |
| R2-FR-6.2 | EDGE-TEST-05 |
| R2-FR-6.3 | EDGE-TEST-05 |
| R2-FR-6.4 | EDGE-TEST-05 |
| R2-FR-6.5 | EDGE-TEST-05 |
| R2-FR-6.6 | EDGE-TEST-05 |
| R2-FR-6.7 | EDGE-TEST-05 |
| R2-FR-7.1 | EDGE-TEST-05; EDGE-TEST-24 |
| R2-FR-7.2 | EDGE-TEST-05; EDGE-TEST-24 |
| R2-FR-7.3 | EDGE-TEST-05; EDGE-TEST-24 |
| R2-FR-7.4 | EDGE-TEST-05; EDGE-TEST-24 |
| R2-FR-8.1 | EDGE-TEST-23 |
| R2-FR-8.2 | EDGE-TEST-23 |
| R2-FR-8.3 | EDGE-TEST-23 |
| R2-FR-8.4 | EDGE-TEST-23 |
| R2-FR-8.5 | EDGE-TEST-23 |
| R2-FR-9.1 | EDGE-TEST-09 |
| R2-FR-10.1 | EDGE-TEST-10 |
| R2-FR-10.2 | EDGE-TEST-10 |
| R2-FR-11.1 | EDGE-TEST-11 |
| R2-FR-11.2 | EDGE-TEST-11 |
| R2-FR-11.3 | EDGE-TEST-11 |
| R2-FR-11.4 | EDGE-TEST-11 |
| R2-FR-11.5 | EDGE-TEST-11 |
| R2-FR-12.1 | EDGE-TEST-19 |
| R2-FR-12.2 | EDGE-TEST-19 |
| R2-FR-13.1 | EDGE-TEST-06 |
| R2-FR-13.2 | EDGE-TEST-06 |
| R2-FR-13.3 | EDGE-TEST-06 |
| R2-FR-13.4 | EDGE-TEST-06 |
| R2-FR-14.1 | EDGE-TEST-07; EDGE-TEST-17; EDGE-TEST-25 |
| R2-FR-14.2 | EDGE-TEST-07; EDGE-TEST-17; EDGE-TEST-25 |
| R2-FR-14.3 | EDGE-TEST-07; EDGE-TEST-17; EDGE-TEST-25 |
| R2-FR-15.1 | EDGE-TEST-08; EDGE-TEST-18 |
| R2-FR-15.2 | EDGE-TEST-08; EDGE-TEST-18 |
| R2-FR-15.3 | EDGE-TEST-08; EDGE-TEST-18 |
| R2-FR-15.4 | EDGE-TEST-08; EDGE-TEST-18 |
| R2-FR-16.1 | EDGE-TEST-22 |
| R2-FR-16.2 | EDGE-TEST-22 |
| R2-FR-16.3 | EDGE-TEST-22 |
| R2-FR-17.1 | EDGE-TEST-20 |
| R2-FR-17.2 | EDGE-TEST-20 |
| R2-FR-17.3 | EDGE-TEST-20 |
| R2-FR-18.1 | EDGE-TEST-12 |
| R2-FR-18.2 | EDGE-TEST-12 |
| R2-FR-18.3 | EDGE-TEST-12 |
| R2-NFR-1.1 | EDGE-TEST-06 |
| R2-NFR-1.2 | EDGE-TEST-12; EDGE-TEST-13 |
| R2-NFR-2.1 | EDGE-TEST-20; SYS-TEST-08 |
| R2-NFR-2.2 | EDGE-TEST-09; EDGE-TEST-10; EDGE-TEST-23 |
| R2-NFR-2.3 | SYS-TEST-08 |
| R2-NFR-3.1 | EDGE-TEST-20; SYS-TEST-08 |
| R2-NFR-4.1 | EDGE-TEST-05; SYS-TEST-07 |
| R2-NFR-5.1 | EDGE-TEST-20 |
| R2-HW-01 | EDGE-TEST-02 |
| R2-HW-02 | EDGE-TEST-13; EDGE-TEST-20 |
| R2-HW-03 | EDGE-TEST-14 |
| R2-HW-04 | EDGE-TEST-15 |
| R2-HW-05 | EDGE-TEST-25 |
| R2-HW-06 | EDGE-TEST-16 |
| R2-HW-07 | EDGE-TEST-21 |
| R2-HW-08 | EDGE-TEST-14 |
| R2-HW-09 | EDGE-TEST-15 |
| R2-HW-10 | EDGE-TEST-06; EDGE-TEST-13 |
| R2-PLT-01 | EDGE-TEST-20 |
| R2-PLT-02 | EDGE-TEST-20 |
| R2-PLT-03 | EDGE-TEST-20 |
| R2-PLT-04 | EDGE-TEST-20 |
| R2-PLT-05 | EDGE-TEST-15 |
| R2-IF-01 | EDGE-TEST-23 |
| R2-IF-02 | EDGE-TEST-23 |
| R2-IF-03 | EDGE-TEST-23 |
| R2-IF-04 | EDGE-TEST-24 |
| R2-IF-05 | EDGE-TEST-05; EDGE-TEST-24 |
| R2-FR-14.4 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-FR-14.5 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-FR-14.6 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-FR-15.5 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-FR-15.6 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-FR-15.7 | EDGE-TEST-17; EDGE-TEST-18; EDGE-TEST-25 |
| R2-LOG-01 | SYS-TEST-07 |

Hardware review closes when the physical assemblies match the BOM/diagram, the chosen power/thermal conditions pass the frozen profile, the camera works on all stations, three stations integrate, accepted offline records/images reconcile, and a teammate reproduces the setup. Model accuracy and central policy are validated with the respective owners rather than claimed as my independent algorithm work.

## 13 Deliverables milestones and open decisions

- Three documented physical Pi 5 stations and one validated USB webcam; component comparison and budget worksheet; connection and deployment diagrams; per-station inventory.
- Versioned edge agent, camera/replay pipeline, runtime adapter, telemetry, command execution, persistent evidence buffer/sync, model-switch/rollback mechanisms, and recovery configuration.
- Setup and deployment instructions, shared schemas, model integration fixture, troubleshooting/recovery procedures, test profile, results, and teammate reproduction record.

| Gate | Required evidence | Owners |
| --- | --- | --- |
| Before procurement | Hardware comparison, total budget, equipment inventory, model/runtime compatibility plan, and provisional BOM. | Tomiwa, Diego, Anthony |
| Before the midterm evidence freeze | Hardware diagram, interface table, named ownership, test profile draft, and a truthful account of completed versus planned work. | All owners |
| Before qualification | One Pi bring-up, USB video capture, power/thermal observations, model benchmark, and signed interface/test profiles. | Tomiwa and Diego; James supports integration |
| Before SD1 final evidence freeze | Component comparisons, available hardware/bench evidence, reproducible setup progress, schematics or connection documentation appropriate to this project, and remaining integration plan. | Tomiwa with Anthony |
| Early SD2 integration | Replicate three physical stations; connect central host; demonstrate detection, telemetry, commands, and offline record/image synchronization. | Tomiwa, James, Ethan, Diego |
| SD2 evaluation and final review | Complete recovery/model lifecycle/trust-monitoring tests and three-controller comparison; close traceability with actual evidence. | Dylan coordinates; all owners |

The October 2 ECE course archive lists the midterm report on November 6, the midterm meeting on November 9, 10, or 12, revision on November 13, and final report/mini demo on December 3, 2026 [S9]. These are archived ECE dates; the CS-led team must reconcile its own applicable submission calendar. They are checkpoints for evidence, not claims that hardware can be procured or validated by an unconfirmed date. SD2 review dates remain to be scheduled.

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
