# Stage 0 — Stratified sampling specification

**Status:** Frozen for Phase 3 implementation  
**Implementation:** [scripts/stage0_sample.py](../../../scripts/stage0_sample.py)  
**Manifest schema:** [schemas/sample_manifest.schema.json](./schemas/sample_manifest.schema.json)  
**Architecture:** [architecture.md](../../architecture.md) §5.3, §6.1

---

## Purpose

Produce a **deterministic**, **reproducible** subset of at most **1,000** reviews from `inputs/raw/groww_playstore_reviews.csv` for Groq-bound stages, while oversampling negative tiers and balancing ISO weeks.

---

## Inputs

| Input | Path / env |
|-------|------------|
| Normalized reviews CSV | `inputs/raw/groww_playstore_reviews.csv` (default) |
| Global seed | `SAMPLER_SEED` env or `--seed` (default **42**) |
| Global row cap | `SAMPLE_MAX_REVIEWS` env or `--max-reviews` (default **1000**) |
| Truncation length (Stage A payload) | `STAGE_A_TEXT_MAX_CHARS` env or `--text-max-chars` (default **320**) |

---

## Rating tiers

| Tier key | Stars | Priority |
|----------|-------|----------|
| `negative` | 1–2 | Highest — largest per-cell caps |
| `neutral` | 3 | Moderate |
| `positive` | 4–5 | Lowest |

---

## Buckets

Each review maps to **`(iso_week, tier)`** where `iso_week` is `YYYY-Www` from the `date` column (ISO calendar week).

Within each bucket:

1. Sort rows by `review_id` ascending (stable, reproducible).
2. If `len(bucket) <= cap`, keep all rows.
3. Else subsample **exactly `cap` rows** using **even stride indices** on the sorted list (deterministic; no RNG):

   `step = len(bucket) / cap`  
   `selected[i] = bucket[int(i * step)]` for `i in 0 .. cap-1`

---

## Per-cell caps (defaults)

Applied per `(iso_week, tier)` before the global ceiling:

| Tier | Default cap per cell |
|------|----------------------|
| `negative` | **35** |
| `neutral` | **12** |
| `positive` | **8** |

Override via CLI: `--cap-negative`, `--cap-neutral`, `--cap-positive`.

**Bucket processing order** (when enforcing global max):

1. ISO weeks ascending (`2026-W08` …)
2. Within each week: `negative` → `neutral` → `positive`

Stop adding rows once **`global_max`** (1,000) is reached; partially filled last bucket is allowed.

---

## Truncation (Stage A only)

For each retained review, compute `text_truncated`:

- If `len(text) <= text_max_chars`, use full `text`.
- Else `text[:text_max_chars - 1] + "…"` (Unicode ellipsis U+2026).

Full `text` remains in the CSV for Stage B evidence expansion.

---

## Outputs

| Artifact | Path |
|----------|------|
| Sample manifest | `data/working/sample_manifest.json` |
| Sampled reviews payload | `data/working/sampled_reviews.json` |

**Manifest** records: run metadata, seed, caps, truncation params, per-bucket counts, and every retained `review_id` with tier, week, rating, date.

**Sampled payload** is an array of objects for Stage A prompts:

`review_id`, `rating`, `date`, `iso_week`, `tier`, `text` (full), `text_truncated`.

---

## Token pre-flight (Phase 3)

After Stage 0, estimate tokens before Groq:

- `tokens ≈ 1.3 × word_count` for review text + stats block + instructions.
- Target **≤ ~9,000 input tokens** per Stage A request ([architecture §6.1](../../architecture.md)).
- If over budget: shorten `text_max_chars`, lower `max-reviews`, or chunk in Phase 3.

---

## Quota alignment

| Groq limit | Stage 0 role |
|------------|----------------|
| 12k TPM | Truncation + ≤1,000 cap keep per-chunk payloads small |
| 100k TPD | Fewer rows → fewer Stage A chunks |
| 1k RPD | Deterministic merge avoids extra merge API calls |
| 30 RPM | Sequential pacing in Phase 3 (≥60s between calls) |
