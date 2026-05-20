# Phase 3 — Groq-powered pulse generation

**Goal:** Run **Stage 0 → Groq Stage A → Groq Stage B → deterministic validation** and export MCP-ready artifacts.

**Status:** Implemented — entry point `scripts/run_phase3.py`.

## Quick start

```bash
# Recommended: 280-review sample fits ~100k TPD on Groq free tier
python3 scripts/run_phase3.py --quota-safe

# Validate existing outputs only
python3 scripts/validate_pulse.py
python3 scripts/run_phase3.py --skip-groq --validate-only --to-email you@example.com
```

Requires **`GROQ_API_KEY`** in `.env`.

## Pipeline stages

| Stage | Script / module | Output |
|-------|-----------------|--------|
| Prep | `corpus_stats.py`, `stage0_sample.py`, `preflight_tokens.py` | `data/working/*.json` |
| Stage A | `run_weekly_pulse.py` (chunked Groq) | `stage_a_chunk_*.json`, `stage_a_merged.json` |
| Stage B | Groq pulse draft | `stage_b_output.json` |
| Validation | `validate_pulse.py`, `pipeline/validate_output.py` | exit code 0/1 |
| Finalize | `pipeline/finalize.py` | `runs/phase-03/run_manifest.json`, `artifacts/mcp_delivery.json` |

## Contracts (Phase 2)

- [schemas](../phase-02/schemas/), [prompts](../phase-02/prompts/), [validation-checklist.md](../phase-02/validation-checklist.md)
- Architecture [§5–§6.1](../../architecture.md)

## Golden regression

- [fixtures/pulse/golden_acceptance.md](../../../fixtures/pulse/golden_acceptance.md)

## Phase 4 handoff

- [MCP server setup](../phase-04/mcp-saksham-server.md) — Gmail draft + Google Docs append via [Saksham MCP](https://saksham-mcp-server-production-f2a5.up.railway.app/)
