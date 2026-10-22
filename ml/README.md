# Machine learning

**Owner:** R3 — Diego  
**Status:** Not implemented — scaffold only.

Smoke-detection models, inference wrappers used by the edge agent, and evaluation.

## Planned contents

- `models/` — model cards / download instructions (no weights in Git)
- `training/` — fine-tuning scripts for pretrained starting points
- `inference/` — common inference interface returning prediction, confidence, model version, latency
- `evaluation/` — detection metrics, edge performance, image/input-change/disagreement methods, candidate comparison
- Model/runtime selection remains open; lightweight YOLO-family and FIgLib are researched candidates, not selected artifacts (ADR 0006)

## Boundaries

Does not own backend deployment or the dashboard. Novel architecture research and autonomous retraining are out of scope.
