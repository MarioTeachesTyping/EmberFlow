# Fault injection

**Owner:** R6 — Dylan  
**Status:** Not implemented — scaffold only.

Repeatable scripts to create the failure conditions in the test plan.

## Planned contents

- Network disconnect/reconnect, broker restart, controller restart
- Induced CPU/thermal load and latency to trigger FPS adaptation

## Boundaries

Never commit fabricated results; outputs go to `experiments/results/` (git-ignored).
