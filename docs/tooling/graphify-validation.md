# Graphify integration validation

Date: October 22, 2026. Tool: official `graphifyy==0.9.93`, installed in a separate Windows
Python 3.12 environment. Source: repository audit branch `bcece609a8ca9908cbb42003fcbd8b8baa1aa45b`
plus this integration. No semantic backend or global agent/hook installation was used.

| Check | Observed result |
|---|---|
| `graphify --help` | CLI loads successfully |
| `graphify extract . --code-only --no-cluster --max-workers 1` | Exit 0; 17 nodes, 25 edges; 15 code-classified files; 59 document files deliberately skipped in initial run |
| `graphify query "test_valid_fixture_is_accepted" --budget 1000` | Exit 0; source `testing/unit/test_edge_message_schema.py`, including calls/references and line numbers |
| `graphify explain "test_valid_fixture_is_accepted"` | Exit 0; identifies function at line 41 with five connections |
| `graphify export html` | Exit 0; local `graphify-out/graph.html` generated |
| Detector and ignore checks | Current spec Markdown remains eligible; PDF/Word/images, generated output and agent-skill files excluded |
| Git ignores | Local graph JSON/HTML and `.venv-graphify` excluded |
| Repository checks | Ruff lint/format and all 14 existing pytest cases pass |

The query reported that its complete answer exceeded the requested 1000-token budget. Treat
`--budget` as a retrieval preference, not a guaranteed billing/output limit in this release.
Extraction warned that `pyproject.toml` yielded no symbols; it also skipped unsupported files
such as `.env.example` and Mermaid sources. This is not a complete configuration/architecture map.

The HTML, graph, caches and machine-specific paths remain local. No generated graph is committed.
Semantic requirement/ownership queries were not tested: they require an explicitly configured
backend and the full document extraction described in [the guide](graphify.md). No claims about
semantic accuracy, token savings, project acceptance or hardware performance follow from this test.
