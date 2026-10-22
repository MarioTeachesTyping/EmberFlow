# EmberFlow project reference

Start here for work anywhere in the repository. This index connects the project specifications
to implementation locations and records where the documents still disagree.
Last reviewed: October 22, 2026.

## Project and document status

EmberFlow is a six-person interdisciplinary senior-design project for distributed edge smoke
monitoring. Tomiwa Aluko is the team's computer engineer and owns the edge hardware/platform.
The current repository contains scaffolding, draft documentation, and proposed message-schema
tests. Inspect the relevant code and test results before claiming a subsystem works.

The [v1.1 specification package](specifications/v1.1/README.md) contains revised review drafts
dated October 22, 2026. Tomiwa approved this revision; it is not evidence of full-team or faculty
signoff, procurement, completed implementation, or hardware test results.

## Read the specifications

| Document | Markdown | PDF | Editable Word |
|---|---|---|---|
| Tomiwa's edge subsystem | [Source](specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.md) | [PDF](specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.pdf) | [Word](specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.docx) |
| Roles and requirements | [Source](specifications/v1.1/EmberFlow_Roles_and_Requirements_Specification_v1_1.md) | [PDF](specifications/v1.1/EmberFlow_Roles_and_Requirements_Specification_v1_1.pdf) | [Word](specifications/v1.1/EmberFlow_Roles_and_Requirements_Specification_v1_1.docx) |
| System SRS | [Source](specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md) | [PDF](specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.pdf) | [Word](specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.docx) |

The [diagram sources and figures](specifications/v1.1/diagrams/) cover station hardware,
three-node deployment, and offline evidence flow. The
[validation record](specifications/v1.1/Validation_Record.json) records document-quality checks
from preparation of the package; it does not certify the system's acceptance tests.
Legacy local source paths in these preserved documents identify the author's original inputs;
they are not repository dependencies. The original v1.0 PDFs are not included in this package.

## Baseline in Tomiwa's v1.1 revision

- Three physical Raspberry Pi 5 stations for an indoor demonstration; no custom PCB required.
- One USB webcam initially, with camera support verified on each Pi; prerecorded input on the
  other stations. A common platform lets teammates integrate their algorithms.
- An existing team laptop/desktop runs central services. Wired Ethernet connects the three
  Pis and host through a switch/router with at least four endpoint ports.
- Offline detection evidence includes metadata, one representative still image per event,
  and retained telemetry. Synchronization completes only when metadata and image are durable
  centrally; retransmission must be safe and central completion idempotent.
- Budget, exact parts, numerical performance limits, model/runtime, messaging and image
  transport, addressing, and bounded storage policy still require decisions and evidence.

Existing accepted ADRs specify [Pi 5 hardware](decisions/0001-edge-hardware.md),
[PostgreSQL with TimescaleDB](decisions/0002-central-database.md), and
[FastAPI with React/TypeScript](decisions/0003-central-services-stack.md).
Consult the [decision register](decisions/README.md) before selecting an open technology.
Historical Jetson/TensorRT alternatives do not establish a Pi runtime dependency.

## Unresolved differences between drafts

The October 14 architecture handoff described by the existing repository produced a narrower
MVP. Its [SRS draft](requirements/EF-SRS-001.md), [architecture](architecture/overview.md),
and [root README](../README.md) classify several capabilities differently from v1.1.
Importing v1.1 does not silently reconcile or approve those differences.

| Topic | Existing repository drafts | October 22 v1.1 review drafts |
|---|---|---|
| Image/model trust monitoring, shadow/candidate/canary/rollback, workload migration | Several are stretch goals | Retained within the original required scope |
| Offline detection images | Open decision | One representative image retained with each event |
| Physical network and initial cameras | Layout and hardware details open | Wired Ethernet; one USB webcam shared for verification |
| Requirement identifiers | Provisional `EF-*` identifiers with original mappings TBD | Original document namespaces retained with traceability |
| Controller owner's name | Gabe | James Connolly (Gabe/Gabriel in team/Jira references) |

For document-review tasks, cite the version and namespace being reviewed. For implementation
that depends on these differences, surface the conflict to Anthony and the affected owners;
record their agreed resolution in the decision register and update the affected drafts together.
Do not infer a requirement mapping, demote an original requirement, or claim team approval
because one document is newer. Compatible work can continue without resolving unrelated items.

## Owners and repository locations

| Role and owner | Responsibility | Start here |
|---|---|---|
| R1 Anthony Terry | Architecture, integration, project coordination | [Architecture](architecture/overview.md), [infrastructure](../infrastructure/README.md) |
| R2 Tomiwa Aluko | Edge hardware, camera input, platform, telemetry, buffering | [Edge](../edge/README.md), edge subsystem specification above |
| R3 Diego Mendoza | Datasets, models, inference contract, evaluation | [ML](../ml/README.md) |
| R4 James Connolly | Controller, messaging, ingestion, recovery policy | [Controller](../controller/README.md) |
| R5 Ethan McKissic | Dashboard, central persistence, operator review | [Dashboard](../dashboard/README.md), [data](../data/README.md) |
| R6 Dylan Mcintee | Reliability validation, fault injection, experiments | [Testing](../testing/README.md), [experiments](../experiments/README.md) |

Subsystem READMEs explain boundaries and planned contents; directory existence does not prove
implementation. See [deployment](architecture/deployment.md) for service placement,
[API contracts](api/contracts.md) and [schemas](api/schemas/) for the current Proposal v0,
and the [test plan](testing/test-plan.md) for verification work. Proposed schemas may need
review against v1.1 before integration; this document import does not change their payloads.

## Working and verifying changes

Follow [CONTRIBUTING.md](../CONTRIBUTING.md) for branches, reviews, interface ownership,
and publishing. Work through pull requests to `main`. Keep secrets, model weights, datasets,
videos, edge databases, and bulk experiment results out of Git.

For Python or contract changes, install the development dependencies and run the repository checks:

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

Dashboard checks depend on its eventual package scripts; see
[CI](../.github/workflows/ci.yml). For document changes, check relative links, diagram references,
requirement IDs, and consistency across Markdown, Word, and PDF. Update the version/status and
regenerate affected exports together; do not leave conflicting versions under the same label.
Report checks actually run and distinguish schema tests from Pi hardware acceptance tests.

## External context

- [Design Proposal and Team Contract](https://docs.google.com/document/d/1YqJpT0JMOyfTeAuKt24NWQ1deJEBbWxRE7mwEsNbeQE/edit): September 22 proposal, reviewed October 22.
- [Early Status Report](https://docs.google.com/document/d/1q3VX7D0t_VJfdb-lvgFS4zNtR2bU10tzd3vvGd2L2iY/edit): reviewed October 22; ML status table dated October 6.
- [EmberFlow Jira board](https://emberflowsd.atlassian.net/jira/software/projects/SCRUM/boards/1): check current tickets for live progress.

External access may require sign-in. Dated reports describe their reporting period; they are
not proof of current model readiness. No selected, benchmarked Pi model is established by
the imported revision. Cite actual model artifacts, benchmarks, and ticket evidence when available.
