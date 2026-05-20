# Phase 1 — Evaluation: Foundation and MCP wiring

## Scope

Validate environment, MCP server registration, and baseline project conventions before building the review pipeline.

**Phase 1 operator docs:** [README](./README.md) · [MCP capability inventory](./mcp-capability-inventory.md) · [Smoke checklist](./smoke-checklist.md)

## Testing

| ID | Test | How to run | Expected |
|----|------|------------|----------|
| T1.1 | MCP servers load | Open Cursor MCP panel; confirm Gmail and Docs (or Workspace) servers appear without error | No load-time errors |
| T1.2 | Tool discovery | Trigger agent to list available MCP tools relevant to Gmail/Docs | Non-empty tool list matching server docs |
| T1.3 | Harmless invocation | Use lowest-risk tool (e.g., read-only or noop if documented) | Success response or documented skip with reason |
| T1.4 | Secrets hygiene | Search repo for credential patterns | No API keys, refresh tokens, or client secrets committed |

## Exit criteria (all must pass)

- [ ] Gmail MCP and Google Docs MCP (or approved combined server) are configured and documented in [decision.md](../../decision.md) once server choice is final.
- [ ] Agent can complete T1.2 and T1.3 successfully or document environment blockers with owner follow-up.
- [ ] Repository layout for `inputs/`, working data, and docs is agreed and described in [implementationplan.md](../../implementationplan.md) or linked runbook.
- [ ] No Google API client libraries added to application code for Phase 1 smoke tests (MCP-only posture preserved).

## Evidence to attach at phase close

- Short note: MCP server names, versions, and config file path (redacted).
- Screenshot or paste of successful tool list (redact account identifiers).
