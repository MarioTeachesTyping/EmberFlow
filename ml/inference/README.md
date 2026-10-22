# Inference interface

**Owner:** R3 — Diego  
**Status:** Not implemented — scaffold only.

The model-agnostic inference contract consumed by the edge agent.

## Planned contents

- Agree frame shape/layout, color order, preprocessing owner, runtime/dependencies, result units and errors with R2
- Output: prediction, confidence, model version, inference latency and source/frame association
- Implementations for the primary and the lightweight/optimized model

## Boundaries

Approved model switching, active/candidate comparison and known-good rollback are required in the v1.1 review scope. R3 supplies artifacts/methods; R2 integrates execution; R4 owns deployment policy. A deterministic fixture demonstrates interface compatibility, not detection accuracy.
