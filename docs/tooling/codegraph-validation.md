# CodeGraph integration validation

Date: October 22, 2026. Source base: `16f449ecac4d1f478ed8d62d0d5ccd0d7266d7ea` plus
this tooling change. Official npm package `@colbymchenry/codegraph@1.6.2` was installed under an
isolated test prefix on Windows. No user's global agent configuration was overwritten.

| Check | Observed result |
|---|---|
| npm installation at version 1.6.2 | Success; matching Windows bundle installed |
| `install --print-config codex`, `claude`, `cursor` | All exit 0 and print the expected MCP snippets without writes |
| `init --yes .` with telemetry disabled | Exit 0; 2 files, 16 nodes, 27 edges |
| `status --json` | Complete index, extraction version 27, no pending changes on initial code scan |
| `explore test_valid_fixture_is_accepted --max-files 2` | Returns actual schema-test source and function at line 41 |
| MCP initialization and `tools/list` over stdio | Server version 1.6.2; `codegraph_explore` available |
| MCP `tools/call` for the schema-test function | Expected `testing/unit/test_edge_message_schema.py` source returned |
| Configuration examples / links | JSON and TOML parsed; 93 local documentation links resolve |
| Repository hygiene | Root AGENTS.md byte-identical to parent; .codegraph ignored and untracked |
| Ruff lint/format and pytest | Pass; all 14 existing tests pass |

The MCP probe used an explicit checkout path and stopped its server afterward. Its first attempt
hit Windows console decoding in the probe; setting UTF-8 resolved it. No CodeGraph source patch
was required. These checks do not prove each teammate's client settings or watcher behavior;
restart/reconnect the actual client and check it locally. Only Windows was exercised here.

The current index is small because the repo contains scaffolding and example-schema tests.
No document semantics, implementation completeness, performance savings, hardware results or
full-team scope approval are inferred. Graphs remain local; root AGENTS.md is preserved.
