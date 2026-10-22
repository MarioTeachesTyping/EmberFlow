---
name: emberflow-codegraph
description: Use CodeGraph for EmberFlow code navigation, callers, dependencies and change impact after reading the project reference.
---

# EmberFlow code navigation

Read root AGENTS.md and docs/PROJECT_REFERENCE.md first, then docs/tooling/codegraph.md.
Use the installed CodeGraph MCP tool or CLI to locate relevant implementation and tests.
Verify source locations and distinguish actual code from required or proposed capabilities.
CodeGraph is the preferred optional coding navigator; Graphify remains optional for document
relationships with its separately configured semantic backend.

Use this checkout's index only. If it is absent/stale, initialize/sync it or fall back to file
search; never block unrelated work on installing a navigator. Read requirements, ADRs and
ownership from the project reference directly: the code graph does not establish those facts.

Follow codegraph.json exclusions. Do not commit .codegraph/, edit a teammate's agent settings,
install hooks or rewrite root AGENTS.md as a side effect of querying. Consult the guide before
setup, and preserve existing MCP entries when connecting an agent.
