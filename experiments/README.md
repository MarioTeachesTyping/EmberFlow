# Experiments

**Owner:** R6 — Dylan  
**Status:** Not implemented — scaffold only.

Repeatable reliability and ML experiments comparing fixed deployment, a simple temperature-threshold controller and full EmberFlow on common retained inputs/faults. Include trust signals, candidate/rollback, recovery, buffered-image delivery and all SRS metrics with stated limitations.

## Planned contents

- `configs/` — experiment parameter files
- `scripts/` — runners that produce results
- `results/` — local output only (git-ignored); publish summaries in docs

## Boundaries

Never commit fabricated or hand-edited results.
