# Phase 2 -- Data analysis and LLM strategy

**Goal:** Profile the Groww review corpus and lock the **quota-aware** Groq pipeline before Phase 3 implements Groq calls and validators.

**Status:** Complete (2026-05-17). Run evidence: [runs/phase-02/PHASE2-RUN-LOG.md](../../../runs/phase-02/PHASE2-RUN-LOG.md).

## Documents

| File | Purpose |
|------|---------|
| [eval.md](./eval.md) | Exit criteria and tests T2.1–T2.8 |
| [data-analysis.md](./data-analysis.md) | Corpus statistics (§§1–7) + pipeline & quota rationale (§§8–12) |
| [stage-0-spec.md](./stage-0-spec.md) | Stratified sampling parameters and manifest contract |
| [validation-checklist.md](./validation-checklist.md) | Pre-MCP validation gates |
| [schemas/](./schemas/) | JSON Schema for Stage 0 manifest, Stage A, Stage B |
| [prompts/](./prompts/) | Full system prompts for Groq Stage A and B |

## Scripts (deterministic, no Groq API)

| Script | Output |
|--------|--------|
| `scripts/corpus_stats.py` | `data/working/corpus_stats.json` |
| `scripts/stage0_sample.py` | `data/working/sample_manifest.json`, `sampled_reviews.json` |
| `scripts/preflight_tokens.py` | `data/working/preflight_estimate.json` |

```bash
python3 scripts/corpus_stats.py
python3 scripts/stage0_sample.py
python3 scripts/preflight_tokens.py
```

## Pipeline summary ([DEC-023](../../decision.md), [DEC-024](../../decision.md))

**Deterministic analysis** → **Stage 0** (≤1,000 reviews, rating tier × ISO week, negative-heavy caps) → **Groq Stage A** (chunked ~9k input; ≥60s pacing) → **deterministic merge** → **Groq Stage B** → **validation** → Phase 4 MCP.

**Fallback:** chunk-and-merge on Stage A only when per-request budget or validation still fails — [architecture](../../architecture.md) §5.7.

## Next

[Phase 3 README](../phase-03/README.md) — Groq client, chunking, merge, validators, golden run.
