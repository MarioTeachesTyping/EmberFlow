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
| Lightweight pretrained YOLO-family candidates | primary or alternative; not selected | _verify_ | _measure_ | _measure_ | Researched in September 22 proposal; no pinned artifact |
| _TBD_ | lightweight | | _measure_ | _measure_ | |

FIgLib is a researched dataset candidate, not a finalized dataset/split. Record the source, license, size, train/val/test split and the agreed
degraded-input subset. Datasets and weights stay outside Git.

## Decision

_None yet._

## Verification

Evaluation protocol in [docs/testing/test-plan.md](../testing/test-plan.md#4-evaluation).

## Evidence and integration gate

The proposal and October 6 ML status table reviewed October 22 do not establish a selected
model/version, trained artifact, final runtime or Pi benchmark. Python/PyTorch/OpenCV/ONNX
Runtime are proposed tools. TensorRT belongs to a historical Jetson alternative and is not a
Pi dependency. Agree the frame/preprocessing/result contract with Tomiwa, benchmark one Pi,
then freeze runtime and numerical targets. Check current tickets/artifacts for later progress.
