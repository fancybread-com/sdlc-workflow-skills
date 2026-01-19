# Feature: /mcp-status (MCP Server Status Check)

> **ASDLC Pattern**: [The Spec](https://asdlc.io/patterns/the-spec/)  
> **Practice Guide**: [Living Specs](https://asdlc.io/practices/living-specs/)  
> **Status**: Active  
> **Last Updated**: 2026-01-19

---

## Blueprint

### Context

MCP servers (Atlassian, GitHub, ASDLC, ADO, etc.) can disconnect or lose authentication after inactivity. Commands like `/start-task`, `/create-task`, and `/complete-task` depend on those integrations. `/mcp-status` verifies connectivity **before** running such commands so users get immediate, actionable feedback instead of cryptic MCP or auth errors.

**List of record**: The canonical source for which MCP servers and `mcp_<Server>_<Tool>` refs this project supports is `mcps/` and `python schemas/validate_mcps.py --list`. The command must use this list, not a runtime MCP discovery API, to know which servers to test.

### Architecture

- **Command location**: `commands/mcp-status.md`. Executed as `/mcp-status` when installed in `.cursor/commands/` or `~/.cursor/commands/`.
- **List of record**: `mcps/<server>/tools/*.json` and `python schemas/validate_mcps.py --list` (or `--list --json`). Servers are the top-level dirs under `mcps/` (e.g. `atlassian`, `github`, `asdlc`, `ado`).
- **Flow**: (1) Run `validate_mcps.py --list` to get servers and tools; (2) for each server, call one lightweight read-only MCP tool (e.g. `mcp_atlassian_getAccessibleAtlassianResources`, `mcp_github_list_commits`, `mcp_asdlc_list_articles`; for `ado`, `mcp_ado_core_list_projects` or equivalent from the list); (3) report connected / disconnected; for disconnected, provide reconnection steps (Cursor Settings → Tools & MCP).
- **Dependencies**: `mcps/`, `schemas/validate_mcps.py`, MCP servers configured in Cursor. **Outbound**: commands that require MCP (e.g. `/start-task`) should direct users to run `/mcp-status` when MCP is in doubt.

### Anti-Patterns

- **Don’t assume MCP is OK without checking** — Always use the list of record and test each server; do not trust a cached or assumed state.
- **Don’t use a non–list-of-record source for servers** — The list of record is `mcps/` and `validate_mcps.py --list`. Do not rely on a runtime “list MCP servers” API that may differ from what the project curates.
- **Don’t modify data** — The command is read-only; only call read-only MCP tools. No creates, updates, or deletes.

---

## Contract

### Definition of Done

- [ ] Command exists at `commands/mcp-status.md` and conforms to the command schema.
- [ ] Command uses `python schemas/validate_mcps.py --list` (or `--list --json`) to obtain the list of record for servers and `mcp_<Server>_<Tool>` refs.
- [ ] For each server in the list of record, the command calls one lightweight read-only MCP tool (per the mapping in the command or `mcps/`) and records success or failure.
- [ ] Output clearly reports each server as connected or disconnected; for disconnected, includes reconnection steps (e.g. Cursor Settings → Tools & MCP → Connect).
- [ ] `python schemas/validate_all.py` passes (command file validates against `schemas/command.schema.json`).

### Regression Guardrails

- **List of record** — The list of record for MCP servers and tools is `mcps/` and `validate_mcps.py --list`. This must not change without updating this spec and the command.
- **Read-only** — The command must only perform read-only operations; no MCP or filesystem writes.
- **Reconnection guidance** — When a server test fails, the command must distinguish auth errors (reconnect) from other errors and provide specific guidance.

### Scenarios

**Scenario: All configured MCP servers are connected**
- **Given**: `mcps/` contains `atlassian`, `github`, and `asdlc`; each of those MCP servers is configured in Cursor and authenticated
- **When**: The user runs `/mcp-status`
- **Then**: The command reports each of atlassian, github, and asdlc as connected (e.g. “✅ atlassian - Connected”) and a summary such as “All systems operational!”

**Scenario: One MCP server is disconnected and needs reconnection**
- **Given**: `mcps/` includes `atlassian`; the Atlassian MCP server in Cursor has lost authentication
- **When**: The user runs `/mcp-status`
- **Then**: The command reports atlassian as disconnected (e.g. “❌ atlassian - Needs authentication”) and includes reconnection steps (Cursor Settings → Tools & MCP → Connect for atlassian)
