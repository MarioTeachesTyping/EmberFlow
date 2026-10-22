# Testing

**Owner:** R6 — Dylan  
**Status:** Legacy v0 schema/fixture tests exist; subsystem, integration, fault and hardware suites are planned.

Shared test suites, fault injection and fixtures. Subsystem owners remain responsible for tests of their own code.

## Planned contents

- `unit/` — fast tests run by `pytest` in CI
- `integration/` — cross-component tests (simulated station → controller → DB)
- `fault_injection/` — network loss, broker loss, thermal/latency degradation
- `fixtures/` — small example messages and test inputs

## Boundaries

See `docs/testing/test-plan.md`.
