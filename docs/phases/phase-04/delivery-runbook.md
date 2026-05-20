# Phase 4 delivery runbook

**MCP server:** [https://saksham-mcp-server-production-f2a5.up.railway.app/](https://saksham-mcp-server-production-f2a5.up.railway.app/)  
**No `googleapis` in this repo** — all Workspace calls go through the server ([DEC-003](../../decision.md), [DEC-025](../../decision.md)).

---

## 1. Configure `.env`

```bash
cp .env.example .env
```

| Variable | Required | Purpose |
|----------|----------|---------|
| `MCP_SERVER_URL` | No (has default) | Saksham Railway URL |
| `PULSE_TO_EMAIL` | **Yes** for Gmail | Draft recipient (your address or approved alias) |
| `GOOGLE_DOC_ID` | No | Doc to append weekly pulse |
| `MCP_API_KEY` | No | `X-API-Key` header if server enforces it |

Example:

```bash
PULSE_TO_EMAIL=your.name@gmail.com
GOOGLE_DOC_ID=15DJYFp_Pz-HFTn09s1KrdOl93W8uinIAfzwyXfwSRMw
```

---

## 2. Prerequisites

```bash
python3 scripts/run_phase3.py --skip-groq --validate-only
python3 scripts/validate_pulse.py   # must exit 0
```

---

## 3. Deliver (happy path)

```bash
# Dry run (no API calls)
python3 scripts/run_phase4.py --dry-run

# Live: Gmail draft + Google Doc append (if GOOGLE_DOC_ID set)
python3 scripts/run_phase4.py
```

Partial delivery:

```bash
python3 scripts/run_phase4.py --gmail-only
python3 scripts/run_phase4.py --docs-only
```

**Operator step:** Open Gmail → **Drafts** → review subject `Groww Play Store Pulse — <week>` → send manually if appropriate.

---

## 4. Failure handling

| Symptom | Likely cause | Action |
|---------|----------------|--------|
| `PULSE_TO_EMAIL is not set` | Missing `.env` | Add recipient email |
| Gmail API error / 403 | MCP server OAuth scope | Fix credentials on Railway server |
| Docs 404 | Wrong `GOOGLE_DOC_ID` or no share | Share Doc with MCP service account / owner |
| HTTP 401 | Need `MCP_API_KEY` | Set key in `.env` matching server |
| Timeout | Railway cold start | Retry; check server health `GET /` |

Logs: `runs/phase-04/delivery_manifest.json` (no full pulse body — redacted).

---

## 5. REST reference (same as MCP tools)

| Endpoint | Body |
|----------|------|
| `POST /create_email_draft` | `{"to","subject","body"}` |
| `POST /append_to_doc` | `{"doc_id","content"}` |
| `GET /tools` | — |

OpenAPI: `{MCP_SERVER_URL}/openapi.json`

---

## 6. Proof of MCP-only path

```bash
bash scripts/check-delivery-path.sh
```

Must report no `googleapis` / Gmail client imports in delivery scripts.
