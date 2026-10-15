# Machine learning

**Owner:** R3 — Diego  
**Status:** Not implemented — scaffold only.

Smoke-detection models, inference wrappers used by the edge agent, and evaluation.

## Planned contents

- `models/` — model cards / download instructions (no weights in Git)
- `training/` — fine-tuning scripts for pretrained starting points
- `inference/` — common inference interface returning prediction, confidence, model version, latency
- `evaluation/` — precision, recall, F1, false-alert rate, edge performance, degraded-image evaluation

## Boundaries

Does not own backend deployment or the dashboard. Novel architecture research and autonomous retraining are out of scope.
