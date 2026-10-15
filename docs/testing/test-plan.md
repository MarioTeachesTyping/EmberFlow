# Test plan

**Status:** Draft. **Owner:** R6 (Dylan). Subsystem owners remain responsible for tests of
their own code.

> No test results are recorded in this document. Results go in experiment output and
> summaries in `docs/research/`, and only from runs that actually happened.

## 1. Test layers

| Layer | Location | Runs in CI | Needs Pi | Owner |
|---|---|---|---|---|
| Contract tests (schema vs example messages) | `testing/unit/test_edge_message_schema.py` | ✅ (exists) | No | R1/R6 |
| Unit tests per subsystem | `testing/unit/` or alongside subsystem code | ✅ | No | Each owner |
| Integration (simulated station → controller → DB) | `testing/integration/` | Planned | No | R6 + R4/R5 |
| Fault injection | `testing/fault_injection/` | Partially (simulated) | Optional | R6 |
| Hardware acceptance | Documented procedures | No | **Yes** | R2/R6 |
| ML evaluation | `ml/evaluation/`, `experiments/` | No | For edge perf | R3/R6 |

## 2. Test matrix (planned)

Requirement references (`FR-nn`) mean `EF-FR-nn` in
[EF-SRS-001](../requirements/EF-SRS-001.md) and are provisional, like the SRS itself.

| ID | Scenario | Requirements | Layer | Pass criteria (draft) |
|---|---|---|---|---|
| T-01 | Messages conform to the contract | FR-05, 06, 20 | Contract | Valid examples pass; invalid examples are rejected |
| T-02 | Station registers and appears healthy | FR-07, 09, 11 | Integration | Station listed as `healthy` |
| T-03 | Telemetry ingested and visible in history | FR-06, 08, 14, 15 | Integration | Records in DB with source timestamps |
| T-04 | Detection shown and confirmed/dismissed | FR-12, 13 | Integration + UI | Review state persisted |
| T-05 | Network loss: inference continues | FR-17 | Fault injection | Station inference count keeps increasing during outage |
| T-06 | Network loss: controller marks station stale | FR-09 | Fault injection | Station `stale` within configured window |
| T-07 | Reconnect: buffered records replayed exactly once | FR-16, 18 | Fault injection | DB count = generated count; 0 duplicates; original timestamps |
| T-08 | Delayed telemetry does not overwrite newer state | FR-16 | Integration | Current state reflects newest `source_timestamp` |
| T-09 | Controller restart during replay | FR-18 | Fault injection | No loss, no duplicates |
| T-10 | Sustained degradation triggers FPS command | FR-19, 20 | Fault injection | Command created only after the observation window |
| T-11 | Single noisy sample does **not** trigger | FR-19 | Unit | No command |
| T-12 | FPS command applied and verified | FR-19, 20 | Fault injection / HW | Lifecycle reaches `verified` with measured FPS change |
| T-13 | FPS command not applied → `failed` | FR-20 | Fault injection | Lifecycle reaches `failed` with reason |
| T-14 | Expired command not applied on reconnect | FR-21 | Fault injection | Station reports `failed` (expired); FPS unchanged |
| T-15 | Cooldown prevents oscillation | FR-21 | Unit + integration | No new command inside cooldown window |
| T-16 | Three-node operation | FR-01 | Hardware acceptance | All three Pis healthy and reporting |

## 3. Failure injection design

| Fault | Method (proposal) | Simulated | On Pi |
|---|---|---|---|
| Station network loss | Stop broker connection / firewall rule / unplug | ✅ | ✅ |
| Broker restart | Restart broker container | ✅ | ✅ |
| Controller restart | Restart controller process | ✅ | ✅ |
| Database unavailable | Stop DB container | ✅ | — |
| High CPU / latency | CPU stress tool alongside inference | ✅ | ✅ |
| High temperature | Real thermal load (remove/limit cooling **safely**) or injected telemetry in simulation | Injected | Real |
| Camera unavailable | Disconnect camera / missing file | ✅ | ✅ |

Every fault script logs: start/end time, target station, fault type and parameters, so the
experiment can be repeated.

## 4. Evaluation protocol

### 4.1 ML metrics (both model configurations)

- Precision, recall, F1, false-alert rate on a held-out test set (dataset per ADR 0006).
- Edge inference performance on Pi 5: latency (mean/p50/p95) and throughput (FPS).
- **Degraded-image evaluation:** the same metrics on a small, **team-agreed** set of degraded
  inputs (e.g. blur, fog/haze, low light). The exact set must be agreed and recorded before
  evaluation.

### 4.2 Reliability metrics

- Records generated vs. accepted vs. duplicated across outage/replay.
- Time to detect a stale station; time to recover after reconnection.
- FPS adaptation: time from condition onset to command, to applied, to verified; resource
  telemetry before vs. after; rate of oscillation.

### 4.3 Baseline comparison

Compare EmberFlow's adaptive behaviour with **simpler fixed/threshold-based behaviour** (e.g.
fixed FPS with no adaptation), under the same fault scenarios, scoped to the defined MVP.

## 5. Acceptance checks for the repository scaffold (Phase 1)

- [x] Nine top-level directories with tracked scaffolding
- [x] README, CONTRIBUTING and architecture docs match approved decisions
- [x] CI validates the existing Python components (contract tests); dashboard steps run only once the dashboard exists
- [x] PR template, branch/commit rules, `.gitignore`, safe `.env.example`
- [x] Contract document defines the edge envelope and FPS command lifecycle; MQTT/NATS left open
- [ ] All six team members have access and a merged, reviewed test PR
- [ ] EF-SRS-001 approved by all six
- [ ] Branch protection enabled on `main`

## 6. How to verify locally

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest
```
