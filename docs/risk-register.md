# EmberFlow technical risk register

Status: **Draft — not yet reviewed by the team.** Maintained by R1 Anthony Terry, per the
[Roles specification](specifications/v1.1/EmberFlow_Roles_and_Requirements_Specification_v1_1.md)
§4. Last updated: November 19, 2026.

This register tracks the project's technical risks across semesters. Its baseline is
[SRS v1.1 §13](specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md) (October 22, 2026),
which supersedes the older risk list in the original Jira ticket. RK-1 to RK-8 keep the ticket's
numbering and topics; RK-9 to RK-12 add the SRS v1.1 risks the ticket did not list. Where a risk
has no row of its own in SRS §13, its source column says so.

The SRS remains authoritative for requirements. If a risk here changes a requirement, scope or
technology choice, record that through the [decision register](decisions/README.md) and the SRS,
not only here.

## Summary

| ID | Risk | Owner | Closure / review point | Status |
|---|---|---|---|---|
| [RK-1](#rk-1-edge-performance) | Edge (Pi/model) performance | Tomiwa Aluko, Diego Mendoza | Before qualification (OD 4, OD 6) | Open |
| [RK-2](#rk-2-model-accuracy-and-data-suitability) | Model accuracy and data suitability | Diego Mendoza | Before platform qualification (OD 4, OD 5) | Open |
| [RK-3](#rk-3-three-station-integration) | Three-station integration | Anthony Terry, Tomiwa Aluko | Early SD2 integration (AC-1, OD 10) | Open |
| [RK-4](#rk-4-fault-and-experiment-repeatability) | Fault and experiment repeatability | Dylan Mcintee | Before SD2 evaluation | Open |
| [RK-5](#rk-5-scope-creep) | Scope creep / scope drift | Anthony Terry | Every scope change | Open |
| [RK-6](#rk-6-technology-indecision) | Technology indecision | Anthony Terry; each OD owner | Each OD closure gate | Open |
| [RK-7](#rk-7-late-integration) | Late integration | Anthony Terry and all owners | Integration contract freeze (OD 2) | Open |
| [RK-8](#rk-8-unsupported-numerical-targets) | Unsupported numerical targets | Tomiwa Aluko, Diego Mendoza, James Connolly, Dylan Mcintee | Before qualification (OD 6) | Open |
| [RK-9](#rk-9-procurement-and-budget) | Procurement and budget | Anthony Terry, Tomiwa Aluko | Before any purchase (OD 8) | Open |
| [RK-10](#rk-10-incomplete-offline-review-evidence) | Incomplete offline review evidence | Tomiwa Aluko, James Connolly, Ethan McKissic | Before outage acceptance (OD 9) | Open |
| [RK-11](#rk-11-unbounded-storage-promise) | Unbounded storage promise | Tomiwa Aluko, Ethan McKissic | Before outage acceptance (OD 9) | Open |
| [RK-12](#rk-12-unreachable-migration-source) | Unreachable migration source | James Connolly, Tomiwa Aluko | Before migration test (OD 7) | Open |

`OD n` means open decision n in SRS §13; the [decision register](decisions/README.md#srs-open-decisions-and-closure-gates)
lists their owners and closure gates. Gate names come from
[SRS §11](specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md) milestones. Likelihood and
severity ratings have not been assigned yet.

## Risks

### RK-1 Edge performance

- **Impact:** The model load on a Raspberry Pi 5 has not been measured and may exceed its
  capacity, along with capture, telemetry and buffering. Station variants or performance claims
  committed before measurement may not hold.
- **Mitigation:** Benchmark one Pi with Diego before committing station variants or numerical
  claims. Freeze a measured capture/performance profile, and keep a lightweight/optimized model
  configuration as the fallback.
- **Owner:** Tomiwa Aluko and Diego Mendoza.
- **Source:** SRS §13 "Pi/model performance"; OD 4, OD 6.

### RK-2 Model accuracy and data suitability

- **Impact:** Detection accuracy depends on dataset annotations, splits, the selected model and
  how it performs on degraded input. Weak model results could hide or be confused with the
  reliability results EmberFlow aims to show.
- **Mitigation:** Document dataset, splits and degraded-input evaluation. Report model
  limitations separately from hardware and system reliability. EmberFlow's contribution is
  reliable operation, not a state-of-the-art detector.
- **Owner:** Diego Mendoza.
- **Source:** SRS §13 "Model/data suitability"; OD 4, OD 5; [ADR 0006](decisions/0006-ml-baseline.md).

### RK-3 Three-station integration

- **Impact:** The final gate needs three physical Pi 5 stations that register, process input and
  report status over the wired network (HI-1.3, AC-1). Simulation does not close it. Differences
  between stations, the single shared USB camera, or unresolved host/network setup could block
  the gate late in SD2.
- **Mitigation:** Bring up one supported station first. Have a teammate reproduce it from the
  documented setup, then replicate to three. Close OD 10 (host, addressing, ports, startup)
  before three-station integration. Test the USB camera on each station in turn (EDGE-TEST-13).
- **Owner:** Anthony Terry (integration) and Tomiwa Aluko (platform).
- **Source:** Ticket item without its own SRS §13 row. Derived from SRS HI-1.3, AC-1, §11 "Early
  SD2 integration", and OD 10.

### RK-4 Fault and experiment repeatability

- **Impact:** If inputs, configuration or fault timing are not retained, the three-controller
  comparison and recovery metrics cannot be reproduced or defended.
- **Mitigation:** Retain input, configuration and fault schedule for every run. Distinguish
  physical from simulated faults. Keep experiment configs and scripts under
  [`experiments/`](../experiments/README.md) and follow the [test plan](testing/test-plan.md).
- **Owner:** Dylan Mcintee.
- **Source:** SRS §13 "Nonrepeatable experiments".

### RK-5 Scope creep

- **Impact:** Added features or a blurred baseline spread the team thin and put the required
  system features at risk.
- **Mitigation:** Keep the indoor, no-PCB baseline separate from the existing mandatory system
  features. Change requirements only through a recorded team decision (ADR plus SRS update).
  Out-of-scope items in the [README](../README.md#out-of-scope) stay out of the backlog.
- **Owner:** Anthony Terry.
- **Source:** SRS §13 "Scope drift".

### RK-6 Technology indecision

- **Impact:** Ten open decisions (OD 1 to OD 10) block procurement, contracts, durable-ingestion
  tests and qualification. If they stay open past their gates, dependent work stalls or
  proceeds on assumptions.
- **Mitigation:** Track each OD with an owner and closure gate in the
  [decision register](decisions/README.md). Close each one with an ADR before its gate, and do
  not build on an open choice as if it were decided.
- **Owner:** Anthony Terry (tracking); each OD's named owner for its decision.
- **Source:** Ticket item without its own SRS §13 row. Derived from SRS §13 OD 1 to OD 10.

### RK-7 Late integration

- **Impact:** If subsystems first meet when they are complete, interface mismatches surface too
  late to fix before SD2 evaluation.
- **Mitigation:** Version the interface fixtures and exercise them before the full model and
  controller exist. Build the vertical slice (Phase 2) with real or mocked inference.
- **Owner:** Anthony Terry and all subsystem owners.
- **Source:** SRS §13 "Late integration"; OD 2;
  [contract gaps](api/contracts.md#7-gaps-before-v11-integration).

### RK-8 Unsupported numerical targets

- **Impact:** Throughput, latency, liveness, recovery or thermal targets stated without
  measurement may be impossible to meet, or untestable. A successful but unbounded demo does not
  satisfy an open target.
- **Mitigation:** Freeze the numerical capture/performance, thermal, liveness, recovery and
  test-duration profile from measured evidence before qualification. State no number without a
  measurement behind it.
- **Owner:** Tomiwa Aluko, Diego Mendoza, James Connolly and Dylan Mcintee (OD 6 owners).
- **Source:** Ticket item without its own SRS §13 row. Derived from SRS §13 "Pi/model
  performance", §10 (open targets closed before qualification), OD 6, NFR-2.5.

### RK-9 Procurement and budget

- **Impact:** No budget, funding or purchased hardware is established. Ordering late, or without
  a cap, could delay bring-up or overspend.
- **Mitigation:** Inventory existing equipment, set a total cap, obtain itemized quotes and
  record lead times before ordering. State no cost without a quote.
- **Owner:** Anthony Terry and Tomiwa Aluko.
- **Source:** SRS §13 "Procurement and budget"; OD 1, OD 8.

### RK-10 Incomplete offline review evidence

- **Impact:** If metadata alone counts as complete, or the edge image is deleted early, an
  operator cannot review a detection made offline.
- **Mitigation:** Mark synchronization complete only when both the record and its image are
  durable centrally. Make retransmission safe and central completion idempotent. Test partial
  uploads and restarts.
- **Owner:** Tomiwa Aluko, James Connolly and Ethan McKissic.
- **Source:** SRS §13 "Incomplete offline review evidence"; OD 2, OD 9.

### RK-11 Unbounded storage promise

- **Impact:** A long outage can exceed edge storage. Promising unlimited buffering would fail
  silently or lose evidence.
- **Mitigation:** Freeze the capacity envelope, quotas, admission/retention policy and reserve.
  Report admission failures explicitly instead of dropping data silently.
- **Owner:** Tomiwa Aluko and Ethan McKissic.
- **Source:** SRS §13 "Unbounded storage promise"; OD 9;
  [ADR 0005](decisions/0005-edge-offline-buffer.md).

### RK-12 Unreachable migration source

- **Impact:** A USB camera stays attached to its host, so moving a workload to another station
  cannot keep reading that camera. A live camera-failover demo is not achievable as described.
- **Mitigation:** Freeze a realistic migration scenario with a source the receiving station can
  reach. Shared recorded footage is the recommended first scenario.
- **Owner:** James Connolly and Tomiwa Aluko.
- **Source:** SRS §13 "Unreachable migration source"; OD 7; FR-5.4.

## Maintaining this register

- Add new risks with the next free ID; never reuse or renumber an ID.
- When a risk closes, set its status to `Closed`, give the date and evidence (ADR, test result,
  measurement), and keep the entry.
- Update owners when roles change, and keep this register consistent with SRS §13.

## Review history

| Date | Review point | Outcome |
|---|---|---|
| — | Not yet reviewed | — |
