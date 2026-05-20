# Phase 1 smoke checklist (operator)

Use with [eval.md](./eval.md). Check boxes when complete.

## T1.1 — MCP servers load

- [ ] Open **Cursor → MCP** (or equivalent) and confirm each configured server shows **no load-time error**.
- [ ] Expected servers: at least **Gmail** and **Google Docs**, or one **Workspace** MCP that covers both—match course guidance.

## T1.2 — Tool discovery

- [ ] In chat, ask the agent to summarize **MCP tools** available for Gmail and Docs (names only).
- [ ] Confirm the list is **non-empty** and matches what you see in server documentation or UI.

## T1.3 — Harmless invocation

Pick the **lowest-risk** operation your servers support (examples: read-only profile, list labels, fetch doc metadata on a scratch doc you own).

- [ ] Invoked: _________________________________
- [ ] Result: success / skipped with documented reason: _________________________________

## T1.4 — Secrets hygiene

From repository root (uses [ripgrep](https://github.com/BurntSushi/ripgrep) if installed; otherwise `find` + `grep`):

```bash
./scripts/check-secrets.sh
```

- [ ] Script exits **0** (no obvious secret patterns) or any hits are **false positives** documented below.

False positives (if any): _________________________________

## Exit criteria (eval.md)

- [ ] [decision.md](../../decision.md) updated with **final** MCP server choice (DEC-013 references layout; add or update server name row when known).
- [ ] Repository layout exists: `inputs/raw/`, `data/working/`, `artifacts/` per [README.md](../../../README.md).
- [ ] [mcp-capability-inventory.md](./mcp-capability-inventory.md) filled in for your environment.
- [ ] No Google API client libraries added to repo for Phase 1 smoke (MCP-only posture).

**Phase 1 sign-off:** _________________ **Date:** _________________
