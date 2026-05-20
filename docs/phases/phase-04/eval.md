# Phase 4 — Evaluation: MCP delivery (Gmail and optional Docs)

## Scope

Validate that the weekly pulse reaches Gmail as a draft and optionally Google Docs **only through MCP tools**, not via embedded Google API clients.

## Testing

| ID | Test | How to run | Expected |
|----|------|------------|----------|
| T4.1 | Gmail draft | Agent invokes Gmail MCP to create draft with pulse body | Draft visible in Gmail drafts; body matches generated pulse |
| T4.2 | Recipient | Use self or approved alias only | Matches [decision.md](../../decision.md) or problem statement |
| T4.3 | Optional Docs | If in scope: create or append via Docs MCP | Doc shows new section with same pulse content |
| T4.4 | No direct API | Search codebase for `googleapis`, `gmail.googleapis`, OAuth redirect URIs in app | None used for delivery (MCP-only) |
| T4.5 | Error handling | Simulate invalid doc id or empty body (in dev) | Graceful failure message; no partial secrets logged |

## Exit criteria (all must pass)

- [ ] Successful T4.1: `python3 scripts/run_phase4.py` creates Gmail draft to `PULSE_TO_EMAIL`.
- [x] T4.3 Docs: `append_to_doc` proven — [PHASE4-DOCS-SMOKE.md](../../../runs/phase-04/PHASE4-DOCS-SMOKE.md).
- [x] Delivery documented: [delivery-runbook.md](./delivery-runbook.md), [mcp-saksham-server.md](./mcp-saksham-server.md).
- [x] T4.4: `bash scripts/check-delivery-path.sh` → OK.

## Evidence to attach at phase close

- Redacted screenshot of Gmail draft or MCP success log.
- If Docs used: link or doc title reference (internal sharing only).
