# EmberFlow documentation

Start with [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md) for the project-wide source map,
ownership, implementation locations, and unresolved differences between drafts.

| Document | Purpose | Status |
|---|---|---|
| [specifications/v1.1/](specifications/v1.1/README.md) | Revised edge, roles, and system specifications; PDF, Word, Markdown, diagrams | Review drafts — October 22, 2026 |
| [architecture/overview.md](architecture/overview.md) | Layers, responsibilities, data flows, open architectural decisions | Draft |
| [architecture/deployment.md](architecture/deployment.md) | Pi 5 processes, central host services, topology, config and startup plan | Draft |
| [api/contracts.md](api/contracts.md) | Message envelopes, FPS command lifecycle, acknowledgments, REST endpoints | **Proposal v0** |
| [api/schemas/](api/schemas/) | Machine-readable JSON Schema for the edge message contract | **Proposal v0** |
| [requirements/EF-SRS-001.md](requirements/EF-SRS-001.md) | Software requirements baseline | **Draft — pending approval by all six** |
| [decisions/](decisions/) | Decision register and architecture decision records (ADRs) | Mixed: see register |
| [testing/test-plan.md](testing/test-plan.md) | Test matrix, fault injection, acceptance checks, evaluation protocol | Draft |
| [research/](research/) | Research notes and evaluation write-ups | Empty |

The existing architecture handoff prioritized the Early Status Report, Design Proposal and
Team Contract, then Roles & Requirements Specification. The imported v1.1 review drafts retain
broader original requirements. These sources are not yet reconciled; consult the differences
recorded in [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md) before changing scope or treating a
draft as the approved system baseline.
