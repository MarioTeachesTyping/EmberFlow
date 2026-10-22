# EmberFlow documentation

Start with [PROJECT_REFERENCE.md](PROJECT_REFERENCE.md) for the project-wide source map,
ownership, implementation locations, the v1.1 alignment decision and remaining review gates.

| Document | Purpose | Status |
|---|---|---|
| [tooling/codegraph.md](tooling/codegraph.md) | Preferred optional coding navigator; mixed-agent setup and validation | CLI/MCP smoke-tested locally on Windows |
| [tooling/graphify.md](tooling/graphify.md) | Optional Graphify install, scope, agent workflow and validation | Local code graph tested; semantic backend not selected |
| [specifications/v1.1/](specifications/v1.1/README.md) | Revised edge, roles, and system specifications; PDF, Word, Markdown, diagrams | Review drafts — October 22, 2026 |
| [architecture/overview.md](architecture/overview.md) | Layers, responsibilities, data flows, open architectural decisions | Draft |
| [architecture/deployment.md](architecture/deployment.md) | Pi 5 processes, central host services, topology, config and startup plan | Draft |
| [api/contracts.md](api/contracts.md) | Message envelopes, FPS command lifecycle, acknowledgments, REST endpoints | **Proposal v0** |
| [api/schemas/](api/schemas/) | Machine-readable JSON Schema for the edge message contract | **Proposal v0** |
| [requirements/EF-SRS-001.md](requirements/EF-SRS-001.md) | Current SRS entry point and legacy-ID crosswalk | **v1.1 review scope; team approval pending** |
| [reviews/2026-10-22-repository-audit.md](reviews/2026-10-22-repository-audit.md) | Sweep findings, evidence, coverage and remaining gaps | October 22 audit |
| [decisions/](decisions/) | Decision register and architecture decision records (ADRs) | Mixed: see register |
| [testing/test-plan.md](testing/test-plan.md) | Test matrix, fault injection, acceptance checks, evaluation protocol | Draft |
| [research/](research/) | Research notes and evaluation write-ups | Empty |

The current review scope is the October 22 v1.1 SRS, per Tomiwa's explicit repository-alignment
decision. The earlier MVP handoff is historical. Full-team/faculty ratification remains pending;
see [ADR 0007](decisions/0007-october-22-review-baseline.md). Dated source reports remain evidence
of their reporting periods, not live implementation status.
