# Phase 4 run log

**Date:** 2026-05-18  
**MCP server:** https://saksham-mcp-server-production-f2a5.up.railway.app/

## Implementation

| Item | Path |
|------|------|
| Entry point | `scripts/run_phase4.py` |
| Delivery module | `scripts/pipeline/mcp_deliver.py` |
| HTTP client | `scripts/pipeline/mcp_client.py` |
| Runbook | `docs/phases/phase-04/delivery-runbook.md` |
| T4.4 check | `scripts/check-delivery-path.sh` |

## Configuration (`.env`)

| Variable | Purpose |
|----------|---------|
| `PULSE_TO_EMAIL` | Gmail draft **To** address (operator must set) |
| `GOOGLE_DOC_ID` | Doc append target |
| `MCP_SERVER_URL` | Saksham server base URL |
| `MCP_API_KEY` | Optional `X-API-Key` header |

## Verified

- **Docs (T4.3):** `append_to_doc` → success (see PHASE4-DOCS-SMOKE.md)
- **T4.4:** `check-delivery-path.sh` → OK (no googleapis in delivery scripts)
- **Gmail (T4.1):** Run after setting `PULSE_TO_EMAIL`:

```bash
python3 scripts/run_phase4.py
```

## Operator checklist

1. Set `PULSE_TO_EMAIL=your.real@email.com` in `.env`
2. `python3 scripts/run_phase4.py`
3. Gmail → Drafts → review → send manually if desired
