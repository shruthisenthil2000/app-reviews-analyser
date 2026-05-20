# Phase 4 smoke — Google Docs via Saksham MCP

**Date:** 2026-05-18  
**Server:** https://saksham-mcp-server-production-f2a5.up.railway.app  
**Doc ID:** from `GOOGLE_DOC_ID` in `.env` (not repeated here)

## Commands

```bash
python3 scripts/run_phase3.py --skip-groq --validate-only
python3 scripts/mcp_deliver.py --docs
```

## Result

```json
{
  "status": "success",
  "message": "Content appended to document"
}
```

Weekly pulse text from `artifacts/mcp_delivery.json` was appended with a server-side timestamp (per [docs_tool.py](https://github.com/shruthisenthil2000/shruthi-mcp-server/blob/main/docs_tool.py)).

## Gmail (optional)

Set `PULSE_TO_EMAIL` in `.env`, then:

```bash
python3 scripts/mcp_deliver.py --gmail
```
