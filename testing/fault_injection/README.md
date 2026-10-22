# Fault injection

**Owner:** R6 — Dylan  
**Status:** Not implemented — scaffold only.

Repeatable scripts to create the failure conditions in the test plan.

## Planned contents

- Network disconnect/reconnect, broker restart, controller restart
- Controlled CPU/thermal load or injected readings, latency, camera loss and storage pressure
- Partial images, lost receipts, replay after restart, node failure and faulty candidate deployment
- Degraded-image, input-change and disagreement cases supplied with R3; distinguish physical from simulated faults

## Boundaries

Never commit fabricated results; outputs go to `experiments/results/` (git-ignored).
