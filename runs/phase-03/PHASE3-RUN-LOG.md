# Phase 3 run log

**Date:** 2026-05-18  
**Entry point:** `scripts/run_phase3.py`

## Implementation delivered

| Component | Path |
|-----------|------|
| Phase 3 orchestrator | `scripts/run_phase3.py` |
| Groq pipeline (Stage A/B) | `scripts/run_weekly_pulse.py` |
| Validation CLI | `scripts/validate_pulse.py` |
| Validators | `scripts/pipeline/validate_output.py` |
| Finalize + MCP payload | `scripts/pipeline/finalize.py`, `pulse_render.py` |
| Golden acceptance | `fixtures/pulse/golden_acceptance.md` |
| Phase 4 MCP doc | `docs/phases/phase-04/mcp-saksham-server.md` |

## Validation run (existing artifacts)

```bash
python3 scripts/run_phase3.py --skip-groq --validate-only
```

| Check | Result |
|-------|--------|
| Valid | **true** |
| Themes | 5 |
| Pulse words | 104 |
| Quotes / actions | 3 / 3 |

## Outputs

- `data/working/stage_a_merged.json`
- `data/working/stage_b_output.json`
- `artifacts/pulse_2026-W21.txt`
- `artifacts/mcp_delivery.json`
- `runs/phase-03/run_manifest.json`

## Full Groq run (operator)

```bash
python3 scripts/run_phase3.py --quota-safe
```

Uses **280** reviews by default to stay within **100k TPD**. Resume partial Stage A with `--resume`.

## Phase 4

Use MCP tools on [Saksham server](https://saksham-mcp-server-production-f2a5.up.railway.app/): `create_email_draft`, `append_to_doc` — see `artifacts/mcp_delivery.json`.
