# Decision register and ADRs

ADRs capture decisions and their authority. `Accepted` records from the initial repository are
preserved. [ADR 0007](0007-october-22-review-baseline.md) records Tomiwa's October 22 revision
direction and repository alignment; full-team/faculty ratification of that revision is pending.
Do not turn that status into team approval or treat remaining technical details as settled.

## Existing accepted records

| ADR | Decision |
|---|---|
| [0001](0001-edge-hardware.md) | Three Raspberry Pi 5 stations; no Jetson requirement |
| [0002](0002-central-database.md) | PostgreSQL with TimescaleDB |
| [0003](0003-central-services-stack.md) | FastAPI controller; React + TypeScript dashboard |

## Revision baseline recorded for review

[0007](0007-october-22-review-baseline.md) records indoor/no-PCB hardware, USB webcam, wired LAN,
existing host, required offline image evidence and restoration of the original required system
scope. These directions are recorded; exact parts, implementations and numerical limits below
remain open. Use the current SRS in [the requirements index](../requirements/EF-SRS-001.md).

## SRS open decisions and closure gates

`SRS OD n` refers to section 13 of the v1.1 SRS. These are document identifiers, not fabricated
Jira keys. Target dates remain TBD until agreed; the closure gates prevent qualification against
undefined targets.

| SRS item | Still to decide / record | Owners | Closure gate | Related record |
|---|---|---|---|---|
| OD 1 | Pi RAM/storage, supply/cables/cooling, exact USB camera and available equipment | Tomiwa, Diego, Anthony | Before procurement | [0001](0001-edge-hardware.md), [0007](0007-october-22-review-baseline.md) |
| OD 2 | MQTT vs NATS, image transfer, routes, access and complete durable-receipt semantics | James, Tomiwa, Anthony; Ethan for image persistence | Before integration contract freeze | [0004](0004-messaging.md), [contract gaps](../api/contracts.md#7-gaps-before-v11-integration) |
| OD 3 | Database/extension versions, image persistence and migration configuration | Ethan, James | Before durable-ingestion tests | [0002](0002-central-database.md) |
| OD 4 | Primary/alternative artifacts, Pi runtime, dependencies, preprocessing and dataset split | Diego, Tomiwa | Before platform qualification | [0006](0006-ml-baseline.md) |
| OD 5 | Quality/input-change/disagreement methods and evaluation inputs | Diego, Dylan | Before trust-monitoring tests | SRS FR-3.5–FR-3.7 |
| OD 6 | Numerical capture/performance, thermal, liveness, recovery and test-duration profile | Tomiwa, Diego, James, Dylan | Before qualification | SRS NFR-2.5 |
| OD 7 | Workload movement with a destination-accessible source; no assumed USB failover | James, Tomiwa, Dylan | Before migration test | SRS FR-5.4 |
| OD 8 | Total budget/funding, BOM, inventory, quotes/tax/shipping and lead times | Anthony and team, Tomiwa | Before any purchase | No budget or purchase established |
| OD 9 | Image format/integrity/size, outbox choice, quotas/reserve, capacity envelope, retention, failures | Tomiwa, James, Ethan | Before outage acceptance | [0005](0005-edge-offline-buffer.md) |
| OD 10 | Existing host identity/OS, Ethernet adapter/switch, addressing, ports and startup | James, Ethan, Anthony, Tomiwa | Before three-station integration | [Deployment](../architecture/deployment.md) |

Additional repository choices: dashboard build/test tooling (Ethan), migration tool (Ethan),
operator authentication/authorization and command validation (James/Ethan with R1/R2), and
project license (team). Redis is optional and needs evidence before adoption. These choices
need recorded owners/dates before their dependent work; no new defaults are supplied here.

## Jira references and source differences

The October 22 report snapshot identifies [SCRUM-15](https://emberflowsd.atlassian.net/browse/SCRUM-15)
as messaging/OD-2 and [SCRUM-17](https://emberflowsd.atlassian.net/browse/SCRUM-17) as database/OD-3.
It contains both older backend comparison language and Ethan's statement that PostgreSQL with
TimescaleDB was agreed. ADR 0002 preserves the repository's accepted selection; confirm actual
configuration with Ethan/James. Do not invent mappings for other SRS OD labels or claim current
Jira status from dated reports. Read the live board when planning work.

To add an ADR, use [0000-template.md](0000-template.md), cite its evidence/authority, and obtain
the relevant owners' review through the contribution workflow. Reconcile future scope changes
with the SRS and requirements crosswalk together.
