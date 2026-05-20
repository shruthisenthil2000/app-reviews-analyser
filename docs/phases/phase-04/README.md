# Phase 4 — MCP delivery

**Goal:** Deliver the validated weekly pulse via **Saksham Google MCP server** only — Gmail draft + optional Google Doc append.

**Status:** Implemented — `scripts/run_phase4.py`

## Quick start

1. Set in `.env`:
   - `PULSE_TO_EMAIL` — where the Gmail **draft** is addressed (your inbox)
   - `GOOGLE_DOC_ID` — optional running Doc
   - `MCP_SERVER_URL` — defaults to [Saksham server](https://saksham-mcp-server-production-f2a5.up.railway.app/)

2. Run:

```bash
python3 scripts/run_phase3.py --skip-groq --validate-only
python3 scripts/run_phase4.py --dry-run
python3 scripts/run_phase4.py
```

3. Open **Gmail → Drafts** and confirm the pulse.

## Documents

| File | Purpose |
|------|---------|
| [eval.md](./eval.md) | Exit criteria T4.1–T4.5 |
| [delivery-runbook.md](./delivery-runbook.md) | Operator steps + failure handling |
| [mcp-saksham-server.md](./mcp-saksham-server.md) | Server tools + REST endpoints |

## Scripts

| Script | Role |
|--------|------|
| `scripts/run_phase4.py` | Phase 4 entry (validate → refresh payload → Gmail + Docs) |
| `scripts/mcp_deliver.py` | Lower-level delivery wrapper |
| `scripts/check-delivery-path.sh` | T4.4 — no `googleapis` in delivery path |

## Evidence

- `runs/phase-04/delivery_manifest.json` — redacted MCP results
- [PHASE4-DOCS-SMOKE.md](../../../runs/phase-04/PHASE4-DOCS-SMOKE.md) — Docs append smoke test

## Next

[Phase 5 README](../phase-05/README.md) — end-to-end runbook and demo.
