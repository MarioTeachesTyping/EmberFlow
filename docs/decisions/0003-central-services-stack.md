# 0003: Central services stack: FastAPI controller, React + TypeScript dashboard

- **Status:** Accepted
- **Date:** 2026-10-14 (recorded from the architecture handoff)
- **Owner:** R4 (Gabe) for the controller; R5 (Ethan) for the dashboard
- **Reviewers:** R1 (Anthony)

## Context

A central service must register stations, ingest events, track health, evaluate the FPS
policy and serve an operator UI. The team needs a stack that is quick to build and test.

## Decision

- **Controller:** Python with **FastAPI**, built as **one application with internal modules**
  (`api`, `messaging`, `policies`, `recovery`) rather than separately deployed microservices.
- **Dashboard:** **React + TypeScript**, talking to the controller only through its REST API.
- Kubernetes or cloud orchestration is **not** a requirement.

## Consequences

- Shared message contracts should have Python type hints (e.g. Pydantic models generated from
  or checked against the JSON Schema).
- Dashboard build tooling (e.g. Vite) and its test runner are still to be chosen by R5.

## Verification

Phase 2 vertical slice: station → controller → database → dashboard.
