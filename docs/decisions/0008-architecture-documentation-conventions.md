# 0008: Architecture documentation conventions

- **Status:** Accepted by R1 (Anthony Terry) as architecture owner; team review pending through the PR
- **Date:** 2026-11-12
- **Owner:** R1 Anthony Terry
- **Reviewers:** R2 Tomiwa Aluko, R3 Diego Mendoza, R4 James Connolly, R5 Ethan McKissic, R6 Dylan Mcintee
- **Jira:** Architecture specification and diagrams ticket (SRS §4; Roles doc Role 1)

## Context

R1 must deliver and maintain a logical component view, a deployment view and the primary data
flow in `docs/architecture/`, reviewed by the team. The v1.1 specification package already
contains three Mermaid figures (SRS §4), and `docs/architecture/` holds earlier ASCII drafts.
Without conventions, the two sets could drift into conflicting versions of the same views.

## Decision

1. **Diagram format.** Architecture diagrams are Mermaid blocks written directly in the
   Markdown files under `docs/architecture/`. GitHub renders them and their changes diff as
   text. No separately exported images are maintained for these views.
2. **Source of truth.** `docs/architecture/` is the maintained source for the architecture,
   deployment and data-flow views. The figures in `docs/specifications/v1.1/diagrams/` are a
   frozen v1.1 snapshot. They are not edited to track later changes, and the architecture
   docs link to them as historical reference.
3. **Layers.** The logical component view uses six runtime layers (edge, ML, messaging,
   control, data and operator) plus a **Testing** layer:
   - Messaging (R4 James) and data (R5 Ethan) have different owners and different open
     decisions (OD 2 vs OD 3), so they are not merged into one "data/messaging" layer.
   - Testing (R6 Dylan) covers CI, automated tests, fault injection and experiments. It is not
     part of the running system, so it is drawn with dashed "verifies" links to the other
     layers, but it appears on the diagram so its ownership and role are visible.
4. **Network labelling.** The station-to-host link is labelled as wired Ethernet that may be
   disconnected (for example by fault injection or a cable or switch failure). Diagrams must
   not imply a wireless link or an internet dependency.
5. **Open items on diagrams.** Undecided choices appear on diagrams labelled `OPEN` with their
   SRS open-decision number (for example "Broker: MQTT or NATS — OPEN, OD 2"). Diagrams never
   pick an open technology.
6. **Scope drawn.** The logical view includes the v1.1 required capabilities (trust
   monitoring, model lifecycle with candidate/shadow/rollback, resolution/model control and
   workload movement) alongside FPS control. They are marked "per v1.1; team ratification
   pending (ADR 0007)" until the team ratifies that revision.

## Consequences

- `overview.md` uses a Mermaid layer diagram, groups its component table by the seven layers
  above, and draws the primary data flow as a Mermaid sequence diagram. `deployment.md` draws
  the deployment view in Mermaid. The project reference maps each SRS §4 figure to its
  maintained view.
- Changes to architecture views follow the cross-subsystem review rules in CONTRIBUTING.md.
- If ADR 0007 is not ratified, item 6 must be revisited together with the SRS.

## Verification

The architecture PR shows rendered diagrams on GitHub, links resolve, every `OPEN` label maps
to a decision-register row, and each layer owner approves the PR.
