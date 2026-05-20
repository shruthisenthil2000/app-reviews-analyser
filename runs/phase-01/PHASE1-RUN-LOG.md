# Phase 1 run log — Groww (Play Store only)

**Product:** Groww (`com.nextbillion.groww`)
**Store:** Google Play Store
**Run date:** 2026-05-15

## Fetch and normalization

```bash
python3 scripts/fetch_playstore_reviews.py \
  --package com.nextbillion.groww \
  --count 15000 --since-weeks 12 \
  --out inputs/raw/groww_playstore_reviews.csv
```

| Stage | Count |
|-------|-------|
| Raw reviews fetched | 15,000 |
| Dropped: outside 12-week window | 2,943 |
| Dropped: quality filters (<=6 words / emoji / non-English) | 9,947 |
| **Final normalized rows** | **2,110** |

### Normalization rules applied

1. **Minimum word count:** Reviews with 6 words or fewer are removed.
2. **No emojis:** Reviews containing any emoji characters are removed.
3. **English only:** Reviews containing non-Latin scripts (Devanagari, Bengali, Gujarati, Tamil, Telugu, Kannada, Malayalam, Arabic, CJK, Korean, Thai) are removed.
4. **Deduplication:** By `review_id`.
5. **Date window:** Only reviews from the last 12 weeks are kept.

### Quality check on output

| Check | Result |
|-------|--------|
| Reviews with <=6 words | **0** |
| Reviews with emojis | **0** |
| Reviews with non-English script | **0** |

## Corpus summary

| Metric | Value |
|--------|-------|
| Total normalized rows | **2,110** |
| Date span | **2026-02-20 → 2026-05-14** |
| ISO weeks covered | **13** (W08 → W20) |

### Weekly breakdown

| Week | Reviews |
|------|---------|
| 2026-W08 | 77 |
| 2026-W09 | 213 |
| 2026-W10 | 293 |
| 2026-W11 | 189 |
| 2026-W12 | 212 |
| 2026-W13 | 144 |
| 2026-W14 | 194 |
| 2026-W15 | 161 |
| 2026-W16 | 178 |
| 2026-W17 | 102 |
| 2026-W18 | 123 |
| 2026-W19 | 138 |
| 2026-W20 | 86 |

### Rating distribution

| Rating | Count | Share |
|--------|-------|-------|
| 5-star | 800 | 37.9% |
| 4-star | 200 | 9.5% |
| 3-star | 143 | 6.8% |
| 2-star | 114 | 5.4% |
| 1-star | 853 | 40.4% |

After filtering out short/emoji/non-English reviews, the rating mix becomes more balanced (negative reviews tend to be longer and more detailed).

### PII posture

CSV columns: `rating,title,text,date,source_store,review_id` — author names and Google profile identifiers are **not** written.

## Other Phase 1 items

| Item | Result |
|------|--------|
| T1.4 Secrets scan | `./scripts/check-secrets.sh` → **OK** |
| Repository layout | All expected directories present |

## Operator-only (Cursor / Google)

| Item | Action |
|------|--------|
| T1.1 MCP servers load | Cursor → MCP: confirm Gmail + Docs servers load without error |
| T1.2 Tool discovery | Ask the agent to list MCP tools for Gmail/Docs |
| T1.3 Harmless invocation | Run one read-only or low-risk MCP call |
| Exit: inventory | Fill [mcp-capability-inventory.md](../../docs/phases/phase-01/mcp-capability-inventory.md) |
