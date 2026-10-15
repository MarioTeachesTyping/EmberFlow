# 0006: ML baseline model, alternative model and dataset

- **Status:** **OPEN** (not decided)
- **Date:** _TBD_
- **Owner:** R3 (Diego)
- **Reviewers:** R2 (Tomiwa), R6 (Dylan), R1 (Anthony)

## Context

EmberFlow needs one **primary** smoke-detection model and one **lightweight/optimized
alternative**. Both start from existing pretrained architectures, run on a Raspberry Pi 5
CPU, and report prediction, confidence, model version and inference latency. Novel
architecture research is out of scope.

## Options considered

| Candidate | Role | Source / license | Pi 5 latency | Precision / recall / F1 | Notes |
|---|---|---|---|---|---|
| _TBD_ | primary | | _measure_ | _measure_ | |
| _TBD_ | lightweight | | _measure_ | _measure_ | |

Datasets: _TBD_. Record the source, license, size, train/val/test split and the agreed
degraded-input subset. Datasets and weights stay outside Git.

## Decision

_None yet._

## Verification

Evaluation protocol in [docs/testing/test-plan.md](../testing/test-plan.md#4-evaluation-protocol).
