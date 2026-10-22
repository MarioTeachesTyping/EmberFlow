# Repository audit — October 22, 2026

The existing repository planning has been aligned to Tomiwa's v1.1 review specifications.
This is a documentation alignment, not implementation or full-team/faculty ratification.
Tomiwa explicitly selected the revised SRS scope during the audit, keeping approval pending.
The [project reference](../PROJECT_REFERENCE.md) remains the shared entry point.

## Scope and evidence

The sweep covers every tracked file at parent revision `3b1fe0adaa9823dd69f260f45ae1aba92e99beb4`
(the document-publication PR), including all pre-existing files from initial commit `acb7769`.
The [coverage record](2026-10-22-file-coverage.json) lists each path, parent content hash,
review method and disposition. Text/config/schema/test contents were inspected; the imported
document/figure package was checked against the previously reviewed copies. No hardware,
deployment, research completion or model accuracy is inferred from a directory or passing schema.

Evidence used:

- [System SRS v1.1](../specifications/v1.1/EmberFlow_Senior_Design_SRS_v1_1.md),
  [edge specification](../specifications/v1.1/EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1.md),
  and [roles specification](../specifications/v1.1/EmberFlow_Roles_and_Requirements_Specification_v1_1.md).
- Tomiwa's session decisions: no PCB, three physical Pi 5 stations, shared USB webcam, wired LAN,
  existing central computer, complete offline metadata/image evidence, and the latest scope choice.
- Local Senior Design project memory; Obsidian's EmberFlow project hub, Codex Discussion Memory,
  historical SRS, interdisciplinary course note, and October 22 proposal/status snapshots.
  The CLI could not connect because Obsidian was closed; the saved Markdown files were read directly.
- [September 22 proposal](https://docs.google.com/document/d/1YqJpT0JMOyfTeAuKt24NWQ1deJEBbWxRE7mwEsNbeQE/edit)
  and [Early Status Report](https://docs.google.com/document/d/1q3VX7D0t_VJfdb-lvgFS4zNtR2bU10tzd3vvGd2L2iY/edit),
  through their October 22 snapshots; the ML table itself is dated October 6. No fresh Google Docs
  or Jira status is claimed by this sweep.
- GitHub branch metadata checked October 22: `main.protected` was `false`. Parent PR CI passed
  Python checks; its dashboard job succeeded by skipping the absent frontend.

## Corrections made

| Finding | Correction | Basis |
|---|---|---|
| FPS alone required; original features demoted to stretch | Restore trust monitoring, resolution/model control, workload movement, shadow/candidate/limited rollout and rollback to planning scope | SRS FR-3.5–3.7, FR-5.1–5.5, FR-6.1–6.6; Tomiwa's explicit choice |
| Camera type/network topology still open | One USB webcam initially, compatible with each Pi; wired LAN to existing host; indoor/no-PCB baseline | HI-1.1, HI-1.3–1.9; R2-HW requirements |
| Optional offline images and metadata-only cleanup | Require one recoverable image per accepted event; complete receipt covers durable, jointly retrievable metadata/image; bounded capacity and observable failure | SI-1.7; FR-7.2–7.7; DR-1.7 |
| Competing SRS copies and unmapped provisional IDs | Make the old SRS path an index to full v1.1 and retain all legacy EF-FR/EF-NFR/EF-SG IDs as topical links with differences explicit | Original IDs remain authoritative; old draft retained in Git history |
| Incomplete ownership descriptions | Formal James Connolly name; clarify Tomiwa's platform handoff, Diego's algorithms, James's policy, Ethan's shared persistence and Dylan's validation | Named v1.1 roles and vault identity clarification |
| One recovery/three-node slice presented as full acceptance | Add trust, lifecycle, image/restart/capacity, hardware, handoff, access/audit and three-controller evaluation coverage | Individual requirements; AC-1–12; EDGE-TEST/SYS-TEST procedures |
| Unspecified research shown only as TBD or confused with final choices | Identify YOLO-family/FIgLib research as candidates; no selected artifact/runtime/Pi benchmark established | Dated proposal/status evidence; ADR 0006 remains open |
| Unfunded/zero-cost implication | State budget/funding and exact parts are unset; inventory/quotes and budget precede purchase | SRS OD 1, OD 8 |
| Test directory described as entirely unimplemented | Distinguish existing v0 schema tests from planned system suites | Actual repository test file and fixtures |
| Protection treated as active and approval implied | Separate policy from actual unprotected `main`; keep team/faculty approval pending | Live branch metadata and unsigned draft approval records |
| Replay could appear to refresh health | Require session/sequence/clock validity and fresh contact separately from historical ordering | SI-1.8; FR-1.3; R2-IF-04 |

The complete v1.1 PDF/Word/Markdown/diagram package is preserved. The v0 schema validation rules
and example fixtures are also preserved; only misleading schema descriptions were corrected.
This avoids choosing unreviewed field names or silently approving a new protocol.

## Items needing attention

1. **Team scope review is still required.** The earlier MVP was substantially smaller than the
   retained original scope. This sweep follows Tomiwa's selected direction, recorded in
   [ADR 0007](../decisions/0007-october-22-review-baseline.md). Anthony and all owners need to
   confirm feasibility and their obligations. If the team reduces scope later, record which
   individual requirements and gates change; AC-4's three demonstrations do not waive the rest.
2. **Proposal v0 cannot carry the full project yet.** It lacks registration/heartbeat payloads,
   session/frame identity, image integrity/completion, storage/backlog status, trust/lifecycle
   outputs and non-FPS control contracts. The `model_switch` invalid fixture and nullable
   `snapshot_ref` are legacy shape tests. See the [contract gap table](../api/contracts.md#7-gaps-before-v11-integration).
   Existing tests do not verify clock semantics, durable storage, partial-image/restart recovery,
   operator access or end-to-end command outcomes.
   A focused schema probe also confirms that an impossible calendar timestamp and a failed
   command result without a reason pass the legacy validator. The current test code does not
   enable semantic format checking; record these gaps when revising the contract/test suite.
3. **Enable actual repository protections.** `main` is unprotected as checked. An admin needs
   PR/review/required-check rules and verified collaborator access. GitHub usernames/CODEOWNERS,
   all six reviewed test PRs and the project license remain unverified or open; none were invented.
   Dashboard steps also use `--if-present`; define the lockfile and required scripts before a
   green job can count as actual dashboard lint/type/test/build evidence.
4. **Freeze hardware, budget and target profiles.** No established purchase, total budget, BOM,
   chosen camera model, storage/supply/cooling variant, acceptance targets or completed Pi model
   benchmark appears in the reviewed evidence. Inventory equipment and benchmark one Pi with
   Diego before hardware/performance commitments. Do not infer newer work is absent merely
   because it is not in these dated sources.
5. **Resolve image capacity and workload movement.** Image size/rate, outage duration, quotas,
   reserve, admission, post-receipt retention, storage location, integrity and transfer/receipt
   semantics still need owners' decisions. Shared replay footage is a recommended migration
   test source, not approved live USB-camera failover.
6. **Database source language differs.** The status snapshot's backend text still proposes a
   simpler PostgreSQL comparison, while Ethan's section says PostgreSQL with TimescaleDB was
   agreed. Existing ADR 0002 remains the recorded selection; exact versions, migration design,
   image persistence and optional Redis need confirmation. SRS OD labels are not Jira keys.
7. **Close access and calendar details.** Identified operator configuration/model control and
   invalid-input handling are SRS requirements; authentication mechanism is not selected. Archived
   ECE deadlines/writing/evaluation obligations need reconciliation with the CS-led team calendar.
   No-PCB does not establish exemptions from those other obligations.
8. **Keep exports portable and versioned.** The preserved package contains legacy local input
   paths and document-quality checks. Those are provenance, not clone dependencies or platform
   results. Future revised exports should use portable source references and update Word/PDF/MD
   together; this sweep does not rewrite the already reviewed files.

## Verification and limits

The companion [validation record](2026-10-22-audit-validation.json) contains the observed check
results and coverage counts for this sweep. Checks include local Markdown link/anchor resolution,
legacy-ID preservation, current SRS requirement references, unchanged package content, unchanged
v0 validation/fixtures, valid JSON, `git diff --check`, Ruff and pytest. No new service or hardware
tests are claimed. The GitHub dashboard job remains a scaffold skip until a frontend exists.

## PR relationship

This follow-up targets `codex/docs-project-reference` so its diff contains the audit changes only.
Review/merge this follow-up into the publication branch first, then merge the document-publication
PR into `main` to deliver both. If the publication PR is merged first instead, refresh the
follow-up against the resulting `main`, retarget it, and verify only audit changes remain
(especially after a squash merge). Recheck CI before merging. Neither PR is full-team/faculty
scope ratification on its own.
