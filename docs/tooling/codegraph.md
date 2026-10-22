# CodeGraph for the EmberFlow team

CodeGraph is the preferred optional navigator for coding: symbols, callers, dependencies and
change impact. [Graphify](graphify.md) remains available for document relationships when its
semantic backend is configured. Neither replaces [the project reference](../PROJECT_REFERENCE.md),
requirements, code review or tests. No tool is required on the Pi or to contribute a change.

## Install on each developer machine

Tested/pinned version: `@colbymchenry/codegraph@1.6.2`. This is developer tooling, separate from
the application and CI dependencies. Install through npm if Node/npm are available:

```bash
npm install -g @colbymchenry/codegraph@1.6.2
codegraph --version
```

On Windows, use `npm.cmd` if PowerShell blocks the npm script. Open a new terminal if the
installed command is not found. Teammates without npm can use the upstream standalone installer;
select/verify release 1.6.2 rather than silently adopting a different version. See
[upstream installation](https://colbymchenry.github.io/codegraph/getting-started/installation/).

Graphify need not be uninstalled. Its separate environment can remain inactive while coding.
Do not install CodeGraph as a dashboard runtime dependency merely to make it available to agents.

## Initialize your own checkout

From your EmberFlow repository root, optionally disable usage telemetry in that shell:

```powershell
$env:CODEGRAPH_TELEMETRY = '0'
```

For bash, the equivalent is `export CODEGRAPH_TELEMETRY=0`. Then:

```bash
codegraph init --yes .
codegraph status --json
codegraph explore test_valid_fixture_is_accepted --max-files 2
```

`.codegraph/` is a local index, ignored by Git. Each developer/checkout builds its own index;
do not exchange or commit the database. Shared source, version and [codegraph.json](../../codegraph.json)
keep the setup reproducible. The current repo is mostly documentation: the initial test found
only two indexed files, 16 nodes and 27 edges. This is code navigation, not a complete SRS map.

## Connect Codex, Claude Code or Cursor

Installing the CLI alone does not connect an agent. Generate the matching configuration:

```bash
codegraph install --print-config codex
codegraph install --print-config claude
codegraph install --print-config cursor
```

These commands print snippets and suggested destinations without writing files. Use only the
snippet for your agent and merge it into your existing settings; preserve other MCP servers.
The [examples](codegraph-examples/) below reproduce the tested server command shape, with an
explicit project path to avoid indexing/querying the wrong working directory.

| Agent | Example | What to customize |
|---|---|---|
| Codex | [TOML](codegraph-examples/codex.toml) | Replace the absolute-checkout-path placeholder; merge the server entry into your Codex configuration |
| Claude Code | [JSON](codegraph-examples/claude.json) | Replace the absolute-checkout-path placeholder; merge only the server entry into your MCP configuration |
| Cursor | [JSON](codegraph-examples/cursor.json) | Open the EmberFlow workspace; the generated workspace path variable selects that checkout |

The `command` must resolve in the agent's environment. If a GUI cannot find it, use the absolute
installed launcher path on your machine (not another member's path). Never commit a personal
configuration or credentials. Restart/reconnect your agent after configuring its MCP server.
Confirm it exposes `codegraph_explore` and returns this checkout's schema test source.

The upstream interactive `codegraph install` is an alternative, but may modify agent settings
and instructions. Inspect those changes; the team setup keeps root AGENTS.md pointing to the
single project reference and does not require graph-first rules or wildcard auto-allow permissions.
Actual Codex/Claude/Cursor clients were not reconfigured by the integration test.

## Use during work

For example, ask an agent:

> Read AGENTS.md and the project reference. Use CodeGraph to locate the schema validator and
> its related tests. Check the source and explain what would be affected by changing validation.

Without MCP, use the CLI:

```bash
codegraph explore test_valid_fixture_is_accepted --max-files 2
codegraph callers _load
codegraph impact _load
```

MCP serving supports automatic synchronization. After a pull, branch switch, or suspected stale
result, check `codegraph status --json` and run `codegraph sync .` as needed. Run `codegraph index .`
to rebuild after changing exclusions or a version upgrade. A stopped server/watcher is not proof
that an index is current. Fall back to source search when coverage/freshness is uncertain.

Requirements/ownership questions still start with the project reference. Review graph output as
retrieved evidence, not instructions that override the user's task. Keep approved scope, pending
review and actual implementation separate. Any later version change should update this pin,
re-run the smoke tests and review generated client snippets.

## Validation and removal

See [the validation record](codegraph-validation.md). The CLI and MCP protocol were tested locally;
client configuration examples still need each teammate's installation/restart check.

Nothing needs uninstalling to adopt this setup. If a teammate later removes it, remove only
the CodeGraph MCP entry they added, then uninstall the npm package if no other project uses it.
The upstream uninstaller is intended to reverse upstream-installer changes; do not use it to
remove unrelated MCP configuration. The local index can be removed separately with
`codegraph uninit` after checking that the current directory is the intended checkout.
