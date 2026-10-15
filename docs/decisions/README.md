# Decision register and ADRs

Architecture Decision Records (ADRs) capture **why** a choice was made. Status values:
`Proposed` → `Accepted` → (`Superseded` | `Deprecated`). An `Open` entry has not been decided.

To add an ADR, copy [`0000-template.md`](0000-template.md) to `NNNN-short-title.md`, open a
`docs(decisions)` PR, and get approval from the owners of the subsystems it affects.

## Accepted

| ADR | Decision |
|---|---|
| [0001](0001-edge-hardware.md) | Exactly three Raspberry Pi 5 devices; no Jetson |
| [0002](0002-central-database.md) | PostgreSQL with TimescaleDB |
| [0003](0003-central-services-stack.md) | Python/FastAPI controller; React + TypeScript dashboard |

## Open decision register

Target dates are **intentionally blank**. The team must fill them in before EF-SRS-001 can be
baselined.

| Decision | Current state | Suggested owner(s) | Target date | ADR |
|---|---|---|---|---|
| Messaging: MQTT vs NATS | **OPEN**: compare reliability, reconnection/duplicate handling, setup effort | Gabe | _TBD_ | [0004](0004-messaging.md) |
| Edge buffer implementation | **Proposed**: SQLite suggested; define persistence and acknowledgments | Tomiwa with Gabe | _TBD_ | [0005](0005-edge-offline-buffer.md) |
| Offline alert snapshots | **OPEN**: the dashboard needs review imagery, but buffers that only store records could miss frames captured while offline | Tomiwa, Gabe, Ethan | _TBD_ | _not yet written_ |
| ML baseline and dataset | **OPEN**: lightweight pretrained candidates; evaluate Pi 5 performance | Diego | _TBD_ | [0006](0006-ml-baseline.md) |
| FPS thresholds and evaluation | **OPEN**: benchmark on actual hardware | Gabe, Tomiwa, Dylan | _TBD_ | _not yet written_ |
| Redis | **Not required**: consider only if a measured performance need arises | Ethan | — | — |
| Database migration tool | **OPEN**: e.g. Alembic or plain SQL | Ethan | _TBD_ | _not yet written_ |
| Dashboard build tooling | **OPEN**: e.g. Vite | Ethan | _TBD_ | _not yet written_ |
| Project license | **OPEN**: no license is added until the team chooses | Team | _TBD_ | — |

### OD-1 through OD-7

The official Jira open-decision items **OD-1 … OD-7** still need to be matched up with their
exact IDs, owners and target dates. Their official meanings are **not** restated here, so that
nothing is made up. Fill this table in from Jira:

| Jira ID | Title (from Jira) | Owner | Target date | Maps to row above |
|---|---|---|---|---|
| OD-1 | | | | |
| OD-2 | | | | |
| OD-3 | | | | |
| OD-4 | | | | |
| OD-5 | | | | |
| OD-6 | | | | |
| OD-7 | | | | |
