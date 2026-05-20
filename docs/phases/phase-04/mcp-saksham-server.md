# MCP delivery — Saksham Google MCP server (Phase 4)

**Server:** [https://saksham-mcp-server-production-f2a5.up.railway.app/](https://saksham-mcp-server-production-f2a5.up.railway.app/)  
**Tools discovery:** `GET /tools` returns available tool names.

Phase 3 produces **`artifacts/mcp_delivery.json`** with pre-formatted `subject`, `body`, and Doc `content`. Phase 4 invokes MCP tools only (no Google APIs in this repo).

## Tools (from server + [shruthi-mcp-server](https://github.com/shruthisenthil2000/shruthi-mcp-server))

| Tool | Purpose | Parameters |
|------|---------|------------|
| `create_email_draft` | Gmail draft | `to`, `subject`, `body` — see [gmail_tool.py](https://github.com/shruthisenthil2000/shruthi-mcp-server/blob/main/gmail_tool.py) |
| `append_to_doc` | Append to Google Doc | `doc_id`, `content` — see [docs_tool.py](https://github.com/shruthisenthil2000/shruthi-mcp-server/blob/main/docs_tool.py) |

Both tools timestamp content server-side when appending.

## Cursor MCP configuration (example)

Add to Cursor MCP settings (HTTP/SSE transport per your host’s requirement):

```json
{
  "mcpServers": {
    "saksham-google": {
      "url": "https://saksham-mcp-server-production-f2a5.up.railway.app/"
    }
  }
}
```

Adjust transport (`url`, `command`, headers) to match how the Railway server exposes MCP in your environment.

## Phase 4 operator flow

1. Complete Phase 3: `python3 scripts/run_phase3.py --skip-groq --validate-only`
2. Set **`PULSE_TO_EMAIL`** (Gmail draft recipient) and optional **`GOOGLE_DOC_ID`** in `.env`.
3. Deliver:

```bash
python3 scripts/run_phase4.py --dry-run
python3 scripts/run_phase4.py
```

See [delivery-runbook.md](./delivery-runbook.md).

REST endpoints (also in `/openapi.json`): `POST /append_to_doc`, `POST /create_email_draft`, `GET /tools`.

## Environment (server-side)

OAuth / service credentials are configured on the **MCP server** ([`auth.py`](https://github.com/shruthisenthil2000/shruthi-mcp-server/blob/main/auth.py) in the upstream repo), not in this project.

Optional local hints for Phase 4 operators (`.env`, not committed):

```bash
PULSE_TO_EMAIL=you@example.com
GOOGLE_DOC_ID=your_doc_id_here
```

Pass into Phase 3 finalize:

```bash
python3 scripts/run_phase3.py --validate-only --to-email "$PULSE_TO_EMAIL" --doc-id "$GOOGLE_DOC_ID"
```
