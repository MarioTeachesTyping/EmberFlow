# EF-SRS-001: current requirements and legacy identifiers

**Current review baseline:** [full system SRS v1.1](../specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md),
October 22, 2026. Read that document for the complete shall requirements, traceability,
acceptance gates and test procedures. This file is its repository index and legacy-ID crosswalk.

Tomiwa approved aligning repository planning to v1.1 on October 22. Full-team/faculty ratification
is pending. The October 14 reduced MVP draft formerly at this path is preserved in Git history
at commit `acb7769`. Its `EF-*` identifiers are retained below for existing references; they do
not replace the original SRS identifiers or establish a narrower acceptance scope.

## Scope and acceptance

Three physical Pi 5 stations, one USB webcam verified on each, replay on the other stations,
an existing central host, wired Ethernet, indoor mains-powered demonstration and no custom PCB
form the physical baseline. Offline evidence requires metadata plus one representative image
per accepted event and retained telemetry under a bounded policy. Metadata-only storage is
not complete synchronization.

Image quality/input change/disagreement, candidate comparison, limited rollout, known-good
rollback, resolution/model controls and workload movement remain required. AC-4's three-mechanism
demonstration does not waive other mandatory requirements. All individual requirements and
AC-1 through AC-12 need evidence. A physical camera cannot move between Pis with its workload;
the receiving node needs an accessible source.

## Legacy functional identifier crosswalk

These are reviewed topical links, not claims of exact semantic equivalence. The original
requirement text controls; proposal-only details are identified explicitly.

| Legacy ID | v1.1 SRS references | Relationship / clarification |
|---|---|---|
| EF-FR-01 | FR-1.1; HI-1.3 | Three physical stations |
| EF-FR-02 | FR-2.1; HI-1.1, HI-1.8 | USB camera/replay, one webcam tested across all three |
| EF-FR-03 | FR-2.2 | Local inference |
| EF-FR-04 | FR-2.4; FR-5.3 | Two model configurations; primary/lightweight plan also in ML ADR 0006 |
| EF-FR-05 | FR-2.3; SI-1.6 | Inference outputs plus frame/time association and preprocessing contract |
| EF-FR-06 | FR-3.1–FR-3.4; DR-1.3 | Telemetry; R2 specification adds CPU, storage and backlog details |
| EF-FR-07 | FR-1.1 | Registration/identity; detailed registration fields in R2-FR-2.2 |
| EF-FR-08 | FR-7.3; SI-1.7; DR-1.2–DR-1.3 | Ingestion must retain metadata and image completion semantics |
| EF-FR-09 | FR-1.2–FR-1.3; NFR-5.3 | Liveness, health and freshness |
| EF-FR-10 | SI-1.1; SI-1.5 | Documented APIs; exact routes remain proposals |
| EF-FR-11 | UI-1.1; NFR-5.3 | Normal, degraded, offline and recovering display |
| EF-FR-12 | UI-1.2; FR-4.2 | Includes representative image, including after outage |
| EF-FR-13 | FR-4.1–FR-4.3 | Human review |
| EF-FR-14 | UI-1.2; UI-1.5 | History and audit |
| EF-FR-15 | SI-1.3 | Existing ADR 0002 selects PostgreSQL with TimescaleDB |
| EF-FR-16 | FR-7.3; SI-1.8; DR-1.3 | Preserve identity/time; distinguish source, session and receipt |
| EF-FR-17 | FR-7.1; NFR-1.1 | Offline inference with an available local source |
| EF-FR-18 | FR-7.2–FR-7.7; NFR-1.2 | Bounded durable evidence, safe retransmission, one logical event |
| EF-FR-19 | FR-5.1 | FPS reduction; no longer the sole required mechanism |
| EF-FR-20 | FR-5.5; NFR-2.4; NFR-5.2 | Trigger/action/outcome evidence; named lifecycle states remain proposed |
| EF-FR-21 | FR-5.1; R2 specification R2-IF-02 | Legacy expiry/cooldown controls retained as protocol proposals; not an exact SRS equivalence |

## Legacy nonfunctional identifiers

| Legacy ID | Current references | Clarification |
|---|---|---|
| EF-NFR-01 | NFR-6.1, NFR-6.3 | Reproducibility |
| EF-NFR-02 | FR-9.5 | Detection metrics, with broader system metrics retained |
| EF-NFR-03 | NFR-2.1–NFR-2.2 | Pi performance measurements |
| EF-NFR-04 | FR-9.2; FR-3.5–FR-3.7 | Degraded-input evaluation plus required trust methods |
| EF-NFR-05 | NFR-2.5; NFR-2.4 | Freeze measured acceptance profile before qualification |
| EF-NFR-06 | NFR-3.4; AC-11 | Simulated development plus physical-platform reproduction/handoff |
| EF-NFR-07 | NFR-4.2; CONTRIBUTING large-file rules | Secrets and repository artifact limits |
| EF-NFR-08 | FR-9.4 | Fixed vs temperature-threshold vs full EmberFlow |
| EF-NFR-09 | HI-1.9; SRS OD 8 | Existing central computer; budget/funding unset, not a zero-cost promise |

## Former stretch identifiers

The earlier `EF-SG-*` labels are historical aliases. Their capabilities are required in the
current review baseline; they are not optional because of those old labels.

| Legacy ID | Current requirements |
|---|---|
| EF-SG-01 | FR-3.5, FR-3.7 — quality/input-change methods |
| EF-SG-02 | FR-5.2 — resolution control |
| EF-SG-03 | FR-5.3 — approved model switch |
| EF-SG-04 | FR-3.6; FR-6.2–FR-6.3 — disagreement/shadow comparison |
| EF-SG-05 | FR-6.5 — limited rollout |
| EF-SG-06 | FR-6.6; NFR-1.4 — known-good rollback |
| EF-SG-07 | FR-5.4 — workload movement with accessible input |

## Approval and outstanding work

The [decision register](../decisions/README.md) records remaining design decisions and closure
gates. No date, cost, model, runtime or performance target is invented to fill an open item.

| Role | Formal name | Review / approval |
|---|---|---|
| R1 | Anthony Terry | Pending |
| R2 | Tomiwa Aluko | Revision direction and repository alignment approved October 22; full-system ratification not claimed |
| R3 | Diego Mendoza | Pending |
| R4 | James Connolly | Pending |
| R5 | Ethan McKissic | Pending |
| R6 | Dylan Mcintee | Pending |

Faculty approval is pending. Keep research/human-review boundaries, individual ECE obligations,
and CS-led project deadlines distinct. See the [audit](../reviews/2026-10-22-repository-audit.md)
for remaining gaps and the [test plan](../testing/test-plan.md) for qualification coverage.
