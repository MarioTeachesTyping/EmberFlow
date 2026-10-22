# 0007: October 22 review baseline and repository alignment

- **Status:** Tomiwa-approved revision direction; full-team/faculty approval pending
- **Date:** 2026-10-22
- **Owner:** R1 Anthony Terry coordinates; R2 Tomiwa Aluko supplied the hardware revision
- **Reviewers:** All six subsystem owners; applicable faculty

## Context

The initial repository followed a reduced MVP handoff dated October 14. The original SRS and
Tomiwa's October 22 revised specifications retain a broader system scope. During this repository
audit, Tomiwa explicitly chose the revised SRS scope while keeping full-team approval pending.
This record captures that authority without fabricating a team decision.

## Recorded revision direction

- Three physical Pi 5 stations, indoor mains-powered demonstration, existing central computer,
  wired Ethernet and at least four endpoint ports.
- One USB webcam initially, compatible with each station; replay on the other two. Exact
  board/accessory variants remain open. No custom PCB is required per Tomiwa's professor clarification.
- Accepted detection evidence includes metadata plus one recoverable representative image per
  event; retain telemetry under a bounded policy. Central synchronization is complete only when
  metadata and complete image are durable and jointly retrievable, confirmed by durable receipt.
- Keep the original required image/model trust, resolution/model control, workload movement,
  shadow/candidate comparison, limited rollout, rollback and comparative evaluation capabilities.
  FPS is a first slice. AC-4's demonstration subset does not remove individual shall requirements.
- Provide a reproducible platform and a teammate algorithm/model-adapter handoff. R3 owns
  methods/models, R2 integrates execution, R4 owns central policy, R5 owns shared persistence/review.

## Unselected details

This does not select MQTT/NATS, an image transport/receipt schema, SQLite, exact hardware,
model/runtime, thresholds, retention/capacity limits, budget, dates, authentication mechanism,
or a live-camera migration design. The original accepted ADRs 0001–0003 remain recorded;
their service versions/configuration and deployment evidence still need definition.

## Consequences and review

Repository planning now follows v1.1 rather than marking its required features as stretch.
Full-team scope ratification, closure of the decision register and real implementation/testing
remain outstanding. Any later scope reduction needs an explicit recorded team decision and
traceable requirement changes. This PR does not implement a service or revise the v0 wire format.

## Verification

Use the SRS individual requirements and AC-1–AC-12, its SYS-TEST procedures, and the R2
EDGE-TEST-01–25 procedures. The [audit](../reviews/2026-10-22-repository-audit.md) records
documentation checks separately from unexecuted hardware/system qualification.
