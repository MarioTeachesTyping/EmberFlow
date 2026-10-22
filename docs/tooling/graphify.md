# Graphify for project navigation

For daily coding, start with [CodeGraph](codegraph.md). Graphify remains optional for broader
document relationships; no uninstall is required. The original Graphify smoke-test record
describes that integration's earlier source revision, not the current complete repository.

Graphify is optional developer tooling alongside the root agent entry point and
[project reference](../PROJECT_REFERENCE.md). It does not run on the Pi, controller or dashboard,
change requirements, prove implementation, or replace source review. Version 0.9.93 is pinned
in [requirements-graphify.txt](../../requirements-graphify.txt); updates need a reviewed change.

The project skill is `emberflow-graph` under `.agents/skills/`. Hosts that discover project Agent
Skills can invoke it (Codex: `$emberflow-graph`); other agents can follow this guide directly.
The upstream global/query-first installer is unnecessary for this setup. Keep root AGENTS.md
pointing to one shared reference. No Git hooks, cloud account or shared server are required.

## Install in a separate environment

From the repository root with Python 3.11 or newer:

```bash
python -m venv .venv-graphify
```

Activate it in PowerShell:

```powershell
.\.venv-graphify\Scripts\Activate.ps1
```

Or in bash:

```bash
source .venv-graphify/bin/activate
```

Then install the official distribution (double `y`) and inspect the CLI:

```bash
python -m pip install -r requirements-graphify.txt
graphify --help
```

Keep this environment separate from application dependencies and the normal CI tooling.
On PowerShell hosts that disallow activation, call `.venv-graphify\Scripts\graphify.exe` directly.

## Local code-only smoke test

```bash
graphify extract . --code-only --no-cluster --max-workers 1
graphify query "test_valid_fixture_is_accepted" --budget 1000
graphify explain "test_valid_fixture_is_accepted"
```

This uses local AST parsing with no semantic model calls. It is intentionally limited: the repo
currently has example-schema tests and scaffolding, so this graph is small and does not capture
the SRS requirements or document meaning. The output is under `graphify-out/`, ignored by Git.
Use `graphify export html` to produce a local interactive view if desired.

## Include current documents

For a requirements/ownership graph, explicitly select a semantic backend/model supported by the
pinned CLI. For example, after configuring an OpenAI-compatible backend outside the repository
and installing its optional client dependency:

```bash
python -m pip install "graphifyy[openai]==0.9.93"
graphify extract . --backend openai --model YOUR_AVAILABLE_MODEL --max-workers 1 --max-concurrency 1
```

`YOUR_AVAILABLE_MODEL` is a placeholder, not a selected team model. Provider credentials belong
in the environment/secret manager. That run sends eligible document content to the selected
backend and may incur provider charges. An Ollama backend is another supported option when a
local model service is available; use the matching extra and explicit backend/model settings.
No provider, API key, cloud subscription or paid model is selected by this integration.

[.graphifyignore](../../.graphifyignore) excludes duplicate PDF/Word exports, media, generated
records, dependencies and agent-skill instructions. Current Markdown sources are the document
inputs. Keep scans rooted at this checkout; do not expand them to the personal Obsidian vault.
The project reference links the relevant external context without copying the whole vault.

After a document build, try these questions and inspect the returned source evidence:

```bash
graphify query "offline representative image durable receipt" --budget 1500
graphify query "Tomiwa platform handoff Diego model" --budget 1500
graphify query "rollback known good model" --budget 1500
```

Compare answers with SRS SI-1.7/FR-7.5, AC-11 and FR-6.6/NFR-1.4 respectively. Missing or inferred
edges are not authority to alter those requirements. A partial graph must be described as partial.

## Refresh and interpret results

Rebuild with the appropriate command after pulls, merges or source edits. `graphify update .`
refreshes code locally but does not perform the semantic document extraction above; it is not
sufficient after SRS/ADR changes. Keep graphs per checkout/worktree and record the source revision,
build mode and model when sharing observations. Fall back to source search when freshness is unclear.

Generated graphs, HTML, caches and cost reports stay local; no generated graph is committed by
this integration. This avoids stale branch-specific results being mistaken for an authoritative
project source. The checked-in guide/configuration/skill are sufficient to reproduce the setup.

## Validation of this integration

See [the smoke-test record](graphify-validation.md) for the commands and observed results.
Document semantic indexing requires the explicitly configured backend above; a code-only test
does not establish its accuracy or coverage.

Upstream references: [source repository](https://github.com/Graphify-Labs/graphify),
[configuration](https://docs.graphify.com/reference/configuration),
[team workflow](https://docs.graphify.com/guides/team-workflows).
