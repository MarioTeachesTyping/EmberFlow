# 0001: Edge hardware: three Raspberry Pi 5 devices

- **Status:** Accepted
- **Date:** 2026-10-14 (recorded from the architecture handoff)
- **Owner:** R2 (Tomiwa)
- **Reviewers:** All

## Context

EmberFlow is a budget-conscious senior-design prototype with no project funding. Edge
stations must run smoke inference locally on live or prerecorded video.

## Decision

Use **exactly three Raspberry Pi 5** devices as edge stations. A Jetson (or other
accelerator board) is **not** required.

## Consequences

- Models must be lightweight enough to run on a Pi 5 CPU. This drives the requirement for a
  lightweight/optimized alternative model (ADR 0006).
- Thermal behaviour of the Pi 5 is a realistic trigger for the required FPS adaptation.
  Cooling setup must be recorded, because it affects the thresholds.
- Development must not depend on physical Pis. A simulated station with prerecorded input is
  required.

## Verification

Pi 5 inference benchmarks for both model configurations; three-node integration demo.
