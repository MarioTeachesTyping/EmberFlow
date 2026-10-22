---
name: emberflow-graph
description: Build or query EmberFlow's optional Graphify index when exploring project relationships, requirements, owners, code, or tests.
---

# EmberFlow graph navigation

Read the root AGENTS.md and docs/PROJECT_REFERENCE.md first. Then read
docs/tooling/graphify.md for the pinned installation, build commands and limitations.

Use Graphify to discover candidate source locations and relationships. Open the cited source
before making a requirement, ownership, approval or implementation claim. The graph is derived
navigation; current source documents, recorded decisions and actual code/test evidence control.

If Graphify or a fresh graph is unavailable, use ordinary file search and source reads.
Do not make setup a prerequisite for another task. Check the graph's source revision and pending
document changes before trusting it; a local code-only build does not index the requirements.

Honor .graphifyignore. Keep generated graphs/caches local and separate per checkout. Do not
index an external Obsidian vault, duplicate exports, secrets or unrelated folders. Semantic
document extraction must use an explicitly selected backend/model; do not inspect or print keys.
Do not install global agent rules or hooks, replace the root AGENTS.md, publish generated graphs,
or change project scope as a side effect of navigation.
