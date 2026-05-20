# Phase 2 run log

**Date:** 2026-05-17  
**Product:** Groww (`com.nextbillion.groww`)

## Deliverables frozen

| Artifact | Path |
|----------|------|
| Corpus profile | [docs/phases/phase-02/data-analysis.md](../../docs/phases/phase-02/data-analysis.md) |
| Stage 0 spec | [docs/phases/phase-02/stage-0-spec.md](../../docs/phases/phase-02/stage-0-spec.md) |
| JSON schemas | [docs/phases/phase-02/schemas/](../../docs/phases/phase-02/schemas/) |
| Validation checklist | [docs/phases/phase-02/validation-checklist.md](../../docs/phases/phase-02/validation-checklist.md) |
| Prompts | [docs/phases/phase-02/prompts/](../../docs/phases/phase-02/prompts/) |
| Decisions | DEC-020, DEC-021, DEC-023, **DEC-024** in [decision.md](../../docs/decision.md) |

## Commands executed

```bash
python3 scripts/corpus_stats.py
python3 scripts/stage0_sample.py
python3 scripts/preflight_tokens.py
```

## Results

| Step | Output | Key metrics |
|------|--------|-------------|
| Corpus stats | `data/working/corpus_stats.json` | 2,110 reviews |
| Stage 0 sample | `data/working/sample_manifest.json`, `sampled_reviews.json` | **683** sampled (≤1,000 cap); seed **42**; truncation **320** chars |
| Pre-flight | `data/working/preflight_estimate.json` | **4** Stage A chunks; **56,000** planned TPD / 100,000 limit — **OK** |

## Tier distribution (sampled)

Defaults: negative **35** / neutral **12** / positive **8** per `(iso_week, tier)` cell, global max **1,000**.

## Phase 3 handoff

Implement Groq Stage A/B using:

- `data/working/corpus_stats.json` — inject into Stage A prompt
- `data/working/sampled_reviews.json` — Stage A review payload (`text_truncated`)
- `docs/phases/phase-02/schemas/*.schema.json` — validators
- `docs/phases/phase-02/prompts/*.md` — system prompts
- `scripts/preflight_tokens.py` — abort if `within_tpd` is false

Groq client, chunking, merge, pacing, and validation code remain **Phase 3** scope.
