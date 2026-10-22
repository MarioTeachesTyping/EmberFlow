## Summary

<!-- What does this PR change, and why? -->

Jira: SCRUM-<!-- id -->

## Subsystem(s) touched

- [ ] edge
- [ ] ml
- [ ] controller
- [ ] dashboard
- [ ] data (schema / migrations)
- [ ] testing / CI
- [ ] infrastructure
- [ ] experiments
- [ ] docs only

## Interface impact

- [ ] No shared contract changes
- [ ] Changes a shared contract (message envelope, REST API, DB schema, FPS command lifecycle)
  - [ ] `docs/api/contracts.md` and `docs/api/schemas/` updated
  - [ ] Owners of every affected subsystem requested as reviewers (see CONTRIBUTING.md "Cross-subsystem changes")
- [ ] Touches an OPEN decision (messaging, buffer, ML baseline, offline snapshots, FPS thresholds) — linked ADR updated, not silently decided

## Verification

<!-- How did you verify this? Paste commands you ran. Do not report results you did not observe. -->

- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `pytest` passes
- [ ] New/changed behaviour has tests (or explain why not)
- [ ] Hardware tested on a Pi 5 (only if relevant): <!-- station id / setup -->

## Safety checklist

- [ ] No secrets, credentials, `.env` files or private keys
- [ ] No datasets, video files, model weights or bulk experiment output
- [ ] Scope matches the current v1.1 review SRS; any requirement addition, removal or demotion has a recorded decision
- [ ] Review draft, team approval and actual implementation/test evidence are distinguished
