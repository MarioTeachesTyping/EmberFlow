# Test plan

**Status:** Planned qualification coverage; legacy v0 schema tests exist.
**Owner:** R6 Dylan Mcintee with each subsystem owner. Full-team review of v1.1 is pending.

Use the [system SRS v1.1](../specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md)
for requirements and SYS-TEST-01–09, and the
[edge specification](../specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.md)
for EDGE-TEST-01–25. The [requirements index](../requirements/EF-SRS-001.md) retains legacy
`EF-*` aliases. `FR-*`, `NFR-*`, `HI-*` and `AC-*` below refer to the full v1.1 SRS.
These procedures are not results. Record only observed runs and distinguish physical from
simulated faults and schema checks from end-to-end correctness.

## 1. Existing checks versus planned suites

| Layer | Location | Current state | Needs Pi |
|---|---|---|---|
| Legacy v0 schema/fixtures | `testing/unit/test_edge_message_schema.py` | Exists in CI; does not establish v1.1 completeness | No |
| Subsystem units | `testing/unit/` or subsystem | Planned beyond schema checks | No |
| Simulated integration | `testing/integration/` | Planned | No |
| Fault injection | `testing/fault_injection/` | Planned; no runnable scripts present | Depends on case |
| Hardware acceptance | EDGE-TEST procedures and retained evidence | Planned | Yes |
| ML/system evaluation | `ml/evaluation/`, `experiments/` | Planned | Yes for Pi performance/final system |

## 2. Coverage matrix

Existing T-01–T-16 identifiers are retained; subsequent rows add omitted qualification coverage.
This matrix routes execution. The individual SRS/R2 traceability tables remain the full checklist.

| ID | Scenario / pass condition | Requirement links | Procedure |
|---|---|---|---|
| T-01 | Example shapes conform to v0; separately close v1.1 contract gaps before integration | SI-1.5–SI-1.8 | Existing schema tests; EDGE-TEST-23 |
| T-02 | Registration/fresh contact identifies station; agreed state shown | FR-1.1–FR-1.3; UI-1.1 | EDGE-TEST-02 |
| T-03 | Telemetry retained with identity, units and source/receive times | FR-3.1–FR-3.4; DR-1.3 | EDGE-TEST-05 |
| T-04 | Live/replay detection and image reach authorized human review | FR-4.1–FR-4.3; UI-1.2 | SYS-TEST-01 |
| T-05 | Local inference continues through network loss with local source available | FR-7.1; NFR-1.1 | EDGE-TEST-06 |
| T-06 | Controller/dashboard mark lost contact within frozen interval; do not infer processing stopped | FR-1.3; NFR-5.3 | EDGE-TEST-24 |
| T-07 | All accepted offline events/images in declared envelope become reviewable once logically, with original identity/time | FR-7.2–FR-7.7 | EDGE-TEST-17 |
| T-08 | Delayed records stay historical; fresh session/contact rules establish current state | SI-1.8; FR-1.3 | EDGE-TEST-24 |
| T-09 | Restart, partial image upload, duplicate metadata and lost receipt preserve pending evidence and converge to complete review | FR-7.4–FR-7.5; DR-1.7 | EDGE-TEST-18 |
| T-10 | Sustained measured condition creates recorded FPS action | FR-5.1; NFR-2.4 | EDGE-TEST-09 |
| T-11 | Noisy sample does not trigger under the selected observation policy | FR-5.1; proposed FPS policy | SYS-TEST-03 |
| T-12 | FPS applied and later measurements establish outcome, not just receipt | FR-5.5; NFR-5.2 | EDGE-TEST-09; SYS-TEST-03 |
| T-13 | Failed action reports reason and preserves audit evidence | FR-5.5; FR-8.1 | SYS-TEST-03; SYS-TEST-07 |
| T-14 | Expired/wrong-target/invalid command never changes state | NFR-4.3; R2-IF-02 | EDGE-TEST-23 |
| T-15 | Selected cooldown/hysteresis avoids repeated oscillation | Proposed FPS policy; NFR-2.4 | SYS-TEST-03 |
| T-16 | Three physical Pis operate over wired LAN; shared USB camera works on each | HI-1.3, HI-1.5, HI-1.8; AC-1 | EDGE-TEST-02, 13, 16 |
| T-17 | Quality/input-change methods and model disagreement demonstrated on retained matched inputs | FR-3.5–FR-3.7; AC-3 | SYS-TEST-02 |
| T-18 | Resolution change and approved smaller-model switch report outcomes without losing pipeline correctness | FR-5.2–FR-5.3 | EDGE-TEST-10, 11 |
| T-19 | Worker processing moves under recorded failure/degradation with source accessible at destination | FR-5.4 | EDGE-TEST-22 |
| T-20 | Shadow candidate has no active alert authority; comparisons and human feedback retained | FR-6.1–FR-6.4 | SYS-TEST-04 |
| T-21 | Limited rollout and known-good rollback retain version/deployment/outcome audit | FR-6.5–FR-6.6; NFR-1.4; AC-6 | EDGE-TEST-19; SYS-TEST-04 |
| T-22 | Accepted/rejected counts reconcile under quota, reserve and full-buffer conditions | FR-7.6–FR-7.7 | EDGE-TEST-25 |
| T-23 | Compatible supply/cables/cooling/storage meet frozen power/thermal/runtime profile | HI-1.4, HI-1.6; NFR-2.5; AC-12 | EDGE-TEST-14, 15, 21 |
| T-24 | Non-owner teammate reproduces platform and integrates fixture/model adapter | AC-11; NFR-3.4 | EDGE-TEST-20 |
| T-25 | Fixed, simple temperature threshold, full EmberFlow share retained inputs/faults; collect defined metrics | FR-9.1–FR-9.5; AC-8, AC-9 | SYS-TEST-05 |
| T-26 | One node/service failure does not crash healthy nodes; camera failure distinct from network failure | NFR-1.3; AC-5 | EDGE-TEST-12, 13; SYS-TEST-06 |
| T-27 | Identified operator controls configuration/model actions; invalid requests rejected and audited | UI-1.3–UI-1.5; NFR-4.1–NFR-4.3 | SYS-TEST-08 |
| T-28 | Trigger/actor/action/outcome reconstructed for model, movement, operator and retention events | FR-8.1–FR-8.3; AC-7 | SYS-TEST-07 |
| T-29 | Final materials preserve human verification and research boundary | AC-10 | SYS-TEST-09 |

AC-4 requires three distinct demonstrated mechanisms, but every mandatory mechanism still
needs its individual evidence. Do not mark the system accepted from T-10–T-16 alone.

## 3. Faults and qualification profile

Freeze input identity/split, model/runtime/hardware/config versions, capture vs processing rates,
latency statistic/limit, thermal/power conditions, liveness/recovery bounds and trial duration.
For outage tests, declare event rate, encoded-image size, telemetry/log rate, usable quota/reserve,
outage duration and completion bound. Account for accepted, rejected, complete and failed evidence.

Fault cases include network/broker/controller outage, lost receipts, interrupted image upload,
database/storage unavailability, restart, storage exhaustion, node/camera loss, resource load,
low light/fog/blur/compression/camera movement and a faulty candidate deployment. Record each
fault's start/end, target, parameters and whether physically induced or simulated. Use controlled
loads or simulated thermal readings; do not make unvalidated cooling changes a test requirement.

## 4. Evaluation

Compare fixed deployment, a simple temperature-threshold controller and full EmberFlow on common
retained inputs/fault schedules. Include precision, recall, F1, false-alert rate, time to detection,
input-change identification time, availability, recovery time, inference latency/throughput,
buffered-alert delivery and rollback success. Define denominator/window, measurement limits and
hardware/software/model configuration. Record before/action/after evidence for each adaptation.

## 5. Repository foundation evidence

- [x] Nine subsystem directories with tracked scaffolding
- [x] Legacy Proposal v0 schema/fixture tests exist; CI runs them
- [x] Contribution guide, PR template, `.gitignore` and safe example configuration exist
- [ ] Full-team/faculty approval of the revised requirements and interfaces
- [ ] All six members' access and merged/reviewed test PRs verified
- [ ] Branch protection and required checks enabled/verified by an admin (`main.protected` was false October 22)
- [ ] Numerical profiles, budget/BOM, model/runtime and complete evidence contracts frozen
- [ ] Hardware/system qualification executed with retained evidence

The [audit](../reviews/2026-10-22-repository-audit.md) records documentation validation. A green
dashboard job currently reports a skip because the frontend does not exist; it is not a UI test.

## 6. Local checks

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest
```
