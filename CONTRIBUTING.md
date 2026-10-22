# Contributing to EmberFlow

These are lightweight standards for a six-person team. Start with
[PROJECT_REFERENCE.md](docs/PROJECT_REFERENCE.md) and the current SRS. ADR 0007 records Tomiwa's
October 22 alignment direction; full-team/faculty review is pending. Accepted ADRs retain their
recorded authority. Do not use the historical MVP handoff to demote current required features;
surface real conflicts and record an explicit decision before changing the baseline.

## 1. Getting access (required for every team member)

Each of the six team members must:

1. Have write access to the GitHub repository.
2. Open a small **test PR** (for example, adding your name to the docs or fixing a typo) that
   follows this guide and is reviewed and merged.

The repository Jira task is not complete until all six have done this.

## 2. Branches

- Repository policy is PRs to `main`, passing CI and at least one approval; no direct pushes.
  GitHub reported `main.protected = false` when checked October 22, 2026. An admin must
  configure and verify protection and required checks (see "Repository setup" below).
- Work on short-lived branches named `<type>/SCRUM-<id>-<short-description>`:
  - `feat/SCRUM-12-edge-buffering`
  - `fix/SCRUM-16-api`
  - `docs/SCRUM-3-srs-baseline`
- `<type>` uses the same list as commit types below. Keep branches small and merge often.

## 3. Commits — Conventional Commits

```
<type>(<scope>): <imperative summary>
```

- **Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`
- **Scopes:** `edge`, `ml`, `controller`, `dashboard`, `data`, `testing`, `infra`, `experiments`, `docs`, `contracts`
- Examples:
  - `feat(edge): add CPU and temperature telemetry`
  - `fix(controller): reject expired FPS commands on replay`
  - `docs(contracts): add command_result failure reasons`

Mark breaking contract changes with `!`, e.g. `feat(contracts)!: rename processing_fps`.

## 4. Pull requests and reviews

- Use the PR template. Link a real Jira issue (`SCRUM-<id>`) when one applies; if none was
  supplied or verified, say so instead of inventing a key.
- At least **one reviewer other than the author**.
- CI must be **green** before merging.
- Prefer squash-merge so each PR becomes one Conventional Commit on `main`.

### Cross-subsystem changes

A change to a **shared interface** needs approval from the owner of every subsystem it affects,
plus R1 (Anthony), who coordinates interfaces. *(This reviewer mapping is a **proposal**
based on the role definitions; the team must confirm it.)*

| Interface | Required reviewers |
|---|---|
| Edge message envelope / payloads (`docs/api/contracts.md`, `docs/api/schemas/`) | R1 + R2 (edge) + R4 (controller) |
| Inference output contract | R1 + R3 (ML) + R2 (edge) |
| REST API | R1 + R4 (controller) + R5 (dashboard) |
| Database schema / migrations | R1 + R5 (data) + R4 (controller) |
| Adaptation/deployment/rollback or workload lifecycle and policy | R1 + R4 + R2 + R3 where model-related + R6 |
| Complete detection/image receipt, retention and persistence | R1 + R2 + R4 + R5; R6 for qualification |
| CI workflow | R1 + R6 |

Once the team supplies everyone's GitHub usernames, encode this table in `.github/CODEOWNERS`.

### Open decisions

Do not settle an OPEN decision (see [docs/decisions/README.md](docs/decisions/README.md))
inside an implementation PR. Write or update the ADR with its actual authority, get the
required owners' review, then implement. Distinguish recorded revision direction from full-team
ratification. Update interfaces, fixtures, requirements and tests together when decisions close.

## 5. Formatting and linting

| Language | Tools | Commands |
|---|---|---|
| Python | Ruff (lint + format), pytest | `ruff check .` · `ruff format .` · `pytest` |
| TypeScript (dashboard) | ESLint, Prettier | Defined by the dashboard owner in `dashboard/frontend/package.json` |

- Use type hints on Python code for **shared contracts** (messages, API models, DB access);
  they are encouraged everywhere else.
- Shared settings live in `pyproject.toml` and `.editorconfig`. Line endings are normalized
  to LF by `.gitattributes`.

## 6. Tests

- Every behaviour change ships with tests, or the PR explains why it doesn't.
- Fast unit tests go in `testing/unit/` or alongside subsystem code; cross-component tests go
  in `testing/integration/`; failure scenarios go in `testing/fault_injection/`.
- If a test needs a Raspberry Pi, mark it clearly as a hardware acceptance test. Normal
  development should only need a simulated station and prerecorded video.
- **Never fabricate or hand-edit test or experiment results.**

Contract changes must update the example messages in `testing/fixtures/contracts/valid` and
`.../invalid`.

## 7. CI checks

CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs:

- `ruff check .`, `ruff format --check .`, `pytest` (Python 3.11)
- Dashboard: `npm ci` plus the `lint`, `typecheck`, `test` and `build` scripts if defined.
  These steps only run once `dashboard/frontend/package.json` and `package-lock.json` exist.

When a subsystem adds its own dependencies, extend CI in the same PR. Don't add jobs that run
against code that doesn't exist yet.

## 8. Secrets

- **Never commit secrets:** no `.env` files, passwords, API tokens, private keys or credentials.
- Copy `.env.example` to `.env` for local settings. Add any new setting to `.env.example` with
  a **safe dummy value**.
- If a secret is committed by mistake, tell R1 straight away and **rotate the secret**.
  Removing it from history is not enough.

## 9. Large files

Do **not** commit:

- video datasets or wildfire footage,
- model weights (`*.pt`, `*.onnx`, `*.tflite`, …),
- bulk experiment output (`experiments/results/` is git-ignored),
- edge buffer databases (`*.sqlite3`).

Instead, document an external download location (for example in a model card under
`ml/models/`) and record checksums/versions so runs can be reproduced. Small fixtures
(a few KB) used by tests are fine. Don't commit proprietary or licence-restricted material.

## 10. Repository setup (admin checklist)

These are GitHub settings, so they can't be committed. A repository admin must set them up:

- [ ] Branch protection on `main`: require a PR, 1 approval, passing `CI / Python lint and tests`, no force-push.
- [ ] Add all six members as collaborators.
- [ ] Add `.github/CODEOWNERS` with GitHub usernames (see table above).
- [ ] Optionally enable squash-merge only.
