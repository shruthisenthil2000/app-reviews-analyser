# Phase 2 Data Analysis: Groww Play Store Reviews

**Corpus:** `inputs/raw/groww_playstore_reviews.csv`
**Product:** Groww (`com.nextbillion.groww`)
**Run date:** 2026-05-15
**Source:** Public Google Play Store reviews, fetched via `google-play-scraper`

---

## 1. Corpus overview

| Metric | Value |
|--------|-------|
| Total normalized reviews | 2,110 |
| Date span | 2026-02-20 to 2026-05-14 |
| ISO weeks covered | 13 (W08 to W20) |
| Total words | ~49,500 |
| Estimated tokens (1.3x words) | ~64,000 |
| Average words per review | 23 |
| Median words per review | 16 |
| Max words in a single review | 142 |

### Normalization rules applied at fetch time

1. Reviews with 6 words or fewer removed
2. Reviews containing emoji characters removed
3. Reviews containing non-English scripts (Devanagari, Bengali, Tamil, etc.) removed
4. Deduplication by `review_id`
5. Date window: last 12 weeks only

---

## 2. Rating distribution

| Rating | Count | Share | Avg words/review |
|--------|-------|-------|------------------|
| 5-star | 800 | 37.9% | 16 |
| 4-star | 200 | 9.5% | 24 |
| 3-star | 143 | 6.8% | 25 |
| 2-star | 114 | 5.4% | 24 |
| 1-star | 853 | 40.4% | 30 |

**Key observation:** After filtering out short/emoji/non-English reviews, the rating distribution is **bimodal** -- roughly equal splits between strong positive (5-star) and strong negative (1-star). Negative reviews are significantly longer and more detailed (avg 30 words vs 16 for 5-star), meaning they carry disproportionate semantic weight in the corpus. The pulse must fairly represent both signals.

---

## 3. Weekly volume trends

| Week | Reviews | Approx tokens |
|------|---------|---------------|
| 2026-W08 | 77 | 2,334 |
| 2026-W09 | 213 | 5,896 |
| 2026-W10 | 293 | 8,230 |
| 2026-W11 | 189 | 5,638 |
| 2026-W12 | 212 | 5,930 |
| 2026-W13 | 144 | 4,470 |
| 2026-W14 | 194 | 5,605 |
| 2026-W15 | 161 | 5,107 |
| 2026-W16 | 178 | 5,326 |
| 2026-W17 | 102 | 3,456 |
| 2026-W18 | 123 | 4,643 |
| 2026-W19 | 138 | 4,967 |
| 2026-W20 | 86 | 2,771 |

Weekly volumes range from 77 to 293 reviews. No week is empty. Per-week token totals (2.3k–8.2k) are below a single **Stage A per-request** budget (~9k input tokens, [architecture §6.1](../../architecture.md)), but the pipeline still samples **across weeks** so no one ISO week dominates the **≤1,000** review cap.

---

## 4. Topic prevalence (keyword-based)

Keyword matching applied across the full corpus. Reviews can match multiple topics.

| Topic | Reviews | Share | Avg rating |
|-------|---------|-------|------------|
| Trading (F&O / Stocks) | 615 | 29.1% | 2.72 |
| App Stability & UX | 603 | 28.6% | 2.87 |
| Withdrawals & Payments | 307 | 14.5% | 2.12 |
| Mutual Funds | 280 | 13.3% | 2.77 |
| Brokerage & Charges | 269 | 12.7% | 2.13 |
| Charts & Data | 261 | 12.4% | 2.62 |
| Customer Support | 208 | 9.9% | 1.69 |
| Account & KYC | 176 | 8.3% | 2.39 |

### Topic keywords used

- **Trading:** trading, f&o, option, futures, intraday, stop loss, order, sell, buy, position, margin, limit order, execution, slippage
- **App Stability & UX:** crash, bug, slow, lag, hang, not working, freeze, glitch, loading, error, not opening, not responding, ui, interface, user friendly, update
- **Withdrawals & Payments:** withdraw, withdrawal, payment, bank, transfer, credit, debit, payout, pending, stuck, money, amount, refund
- **Mutual Funds:** mutual fund, mutual funds, sip, external funds, nav, portfolio, scheme, redemption, switch, elss, lumpsum
- **Brokerage & Charges:** brokerage, charges, fees, commission, hidden charges, too much, overcharge, dp charges, stt, gst, tax
- **Charts & Data:** chart, candlestick, indicator, technical, graph, screener, watchlist, alert, notification, market data, showing, not showing
- **Customer Support:** customer support, customer care, customer service, support team, helpline, call, response, ticket, resolve, complaint
- **Account & KYC:** account, kyc, verification, demat, login, otp, password, locked, blocked, nominee, pan

---

## 5. Negative vs positive theme split

| Topic | 1-2 star reviews | Share of neg | 4-5 star reviews | Share of pos |
|-------|-----------------|-------------|-----------------|-------------|
| Trading | 323 | 33% | 249 | 25% |
| App Stability & UX | 289 | 30% | 255 | 26% |
| Withdrawals & Payments | 214 | 22% | 77 | 8% |
| Brokerage & Charges | 184 | 19% | 70 | 7% |
| Customer Support | 165 | 17% | 28 | 3% |
| Mutual Funds | 141 | 15% | 117 | 12% |
| Charts & Data | 139 | 14% | 95 | 10% |
| Account & KYC | 104 | 11% | 53 | 5% |

**Key findings:**

- **Customer support** has the most extreme negative skew: 17% of negative reviews mention it, but only 3% of positive reviews. Average rating 1.69 -- the worst of any topic.
- **Withdrawals/payments** and **brokerage/charges** are heavily negative-skewed (22%/19% neg vs 8%/7% pos), indicating money-related friction is a major pain point.
- **Trading** and **app UX** appear in both positive and negative reviews, suggesting mixed experiences -- some users love the trading features, others struggle with them.
- **Mutual funds** is relatively balanced, with both praise and complaints.

---

## 6. Top bigram signals (filtered)

| Count | Bigram |
|-------|--------|
| 155 | easy to |
| 118 | to use |
| 92 | very good |
| 81 | groww app |
| 75 | mutual fund |
| 75 | mutual funds |
| 73 | user friendly |
| 68 | very bad |
| 58 | very easy |
| 54 | best app / worst app |
| 50 | unable to |
| 50 | for beginners |
| 47 | customer support / customer care |
| 44 | f o |
| 43 | customer service |
| 39 | stop loss |
| 39 | not working |
| 38 | external funds |
| 36 | very high |
| 34 | brokerage charges |
| 32 | please add |
| 32 | market price |
| 29 | very poor |

---

## 7. Top single-word signals

| Count | Word | Likely topic association |
|-------|------|------------------------|
| 408 | groww | Product name (ubiquitous) |
| 259 | trading | Trading |
| 232 | easy | UX (positive) |
| 190 | money | Payments / withdrawals |
| 188 | charges | Brokerage |
| 178 | option | Trading (F&O) |
| 163 | customer | Support |
| 157 | market | Trading |
| 156 | funds / loss | Mutual funds / Trading |
| 136 | stock / update | Trading / UX |
| 133 | experience | General sentiment |
| 130 | brokerage | Brokerage |
| 128 | add / order | Feature requests / Trading |
| 122 | price | Trading |
| 116 | chart | Charts |
| 114 | high | Charges / prices |
| 111 | showing | Data display issues |
| 106 | support | Customer support |

---

## 8. Token budget and Groq quotas — why we sample and chunk

### Full corpus vs what Groq sees

| Scope | Words (approx) | Tokens (approx, 1.3× words) |
|-------|----------------|------------------------------|
| Full normalized CSV (2,110 rows) | ~49,500 | ~64,000 |
| **Stage 0 cap** (≤1,000 sampled rows, untruncated upper bound) | ~23,000 | ~30,000 |
| **Stage A per request** (target input budget) | — | **≤ ~9,000** |
| **Stage B** (merged Stage A JSON + evidence texts only) | — | plan **≤ ~15,000** combined |

The full corpus (~64k tokens) is **not** sent in one request. [DEC-023](../../decision.md) and [architecture §6.1](../../architecture.md) require **quota-aware** staging: stratified sampling, **truncation for Stage A only**, **chunking** when a single prompt would exceed the per-request budget, and **pacing** between HTTP calls.

### Published limits — `llama-3.3-70b-versatile`

Planning assumptions (see [architecture.md §6.1](../../architecture.md), [implementation plan](../../implementationplan.md) Phase 2/3):

| Limit | Value | How this corpus uses it |
|-------|--------|-------------------------|
| Requests per minute (RPM) | **30** | Sequential calls only; no parallel burst |
| Requests per day (RPD) | **1,000** | Weekly run uses **few** requests; avoid extra Groq “merge” calls |
| Tokens per minute (TPM) | **12,000** | Keep each request **≤ ~9k input tokens**; **≥60s** between calls in one run |
| Tokens per day (TPD) | **100,000** | Budget **all** Stage A chunks + Stage B + **at most one** repair retry per chunk/stage |

### Why sample to ≤1,000 (not “send everything”)

1. **TPM / per-request ceiling** — Even though 2,110 rows fit a large context window in theory, **12k TPM** forces **small payloads** per HTTP request (~9k input target), not a single 64k-token dump.
2. **TPD** — Untruncated 1,000-review payloads (~30k tokens of review text) plus stats, instructions, completions, and retries must stay under **100k TPD** when multiplied across chunks.
3. **Signal quality** — Stratified sampling with **negative-heavy caps** preserves pain signals without boilerplate dominance (§2, §5).
4. **Pipeline shape** — **Stage A** (themes + evidence ids) is isolated from **Stage B** (pulse prose); **validation** runs before MCP.

### Token math for a typical weekly run (this corpus)

Use the architecture pre-flight rule: `tokens ≈ 1.3 × word_count`, plus **~1–2k** reserved for model output per request.

**Stage 0 → Stage A (truncated text in prompt):**

- At **1,000** samples with **no** truncation: ~23k words → ~**30k** review tokens → requires **N ≥ 4** Stage A chunks at ~9k input each (stats + instructions consume part of each chunk).
- With **deterministic truncation** (e.g. 280–400 chars per review, suffix ellipsis): review-token mass drops sharply; **N** may be **1–3** for typical tier/week caps tuned below the 1,000 ceiling.
- **Chunk sizing:** Each chunk’s estimated **input** (stats fragment + instructions + truncated reviews in that chunk) must stay **≤ ~9,000 tokens** before the Groq call.

**Daily budget check (worst-case planning):**

```
N × 9k   (Stage A chunks)
+ 15k    (Stage B + evidence expansion)
+ 5k     (retry headroom — one repair per chunk/stage max)
< 100k TPD
```

Example: **N = 8** → 72k + 15k + 5k = **92k** (within TPD). If pre-flight estimate exceeds **100k**, lower the Stage 0 cap, shorten truncation, or reduce **N** before calling Groq.

**Pacing:** **≥ 60 seconds** between successive Groq requests in the same run (Stage A chunk → chunk, last chunk → Stage B) unless monitoring proves a tighter safe interval under **12k TPM**.

**Retries:** **At most one** JSON repair attempt per failed Stage A chunk or Stage B — protects **1k RPD** and **100k TPD**.

---

## 9. Primary pipeline (DEC-023): quota-aware sampling + staged Groq + validation

Flow (see [architecture.md](../../architecture.md) §5, [implementationplan.md](../../implementationplan.md) Phase 2–3):

**Deterministic analysis** → **Stage 0 (≤1,000)** → **Groq Stage A** (chunked if needed; deterministic merge) → **Groq Stage B** → **Validation** → (Phase 4) MCP.

### Stage 0 — stratified sampling

| Element | Specification |
|---------|----------------|
| Buckets | `(ISO week, rating tier)` where tier ∈ {**Negative** 1–2★, **Neutral** 3★, **Positive** 4–5★} |
| Ordering | Within each bucket, sort by `review_id` ascending (stable, reproducible) |
| Caps | Per-bucket **tier-weighted** caps: negatives highest, positives lowest — tune toward the **≤1,000** hard ceiling (not a lower fixed band) |
| Hard ceiling | Stop selecting once **1,000** reviews are retained across all buckets (remaining buckets may be under-filled) |
| Truncation (Stage A only) | Deterministic max-length clip per `text` (e.g. 280–400 chars, stable ellipsis); full text stays in CSV for Stage B evidence expansion |
| Seed | Fixed integer `SAMPLER_SEED` (env or config), logged in manifest |
| Artifact | `data/working/sample_manifest.json` — seed, caps per tier/week, truncation params, every retained `review_id` |

**Prioritize negatives:** In this corpus, 1–2★ reviews average ~30 words vs ~16 for 5★; they carry disproportionate actionable detail. Stratification prevents any single ISO week from exhausting the **1,000** slot budget while still surfacing pain.

### Stage A — Groq theme discovery

- **Input:** Deterministic stats (§§2–7 aggregates) + Stage 0 sampled reviews (`review_id` + `rating` + `date` + **truncated** `text` for the prompt).
- **Chunking:** If estimated input for one prompt exceeds **~9k tokens**, split sampled reviews into **ordered chunks**; **one Groq request per chunk**.
- **Pacing:** **≥60s** between successive Groq requests in the same run.
- **Merge:** **Prefer deterministic consolidation** in code (dedupe theme labels, union `evidence_review_ids`, re-rank using §2–7 signals). Optional small Groq merge only if deterministic merge is insufficient (costs RPD/TPD).
- **Output:** **JSON only** — up to **5** ranked themes; each theme includes **`evidence_review_ids`** (subset of sampled ids only).
- **Validation / retry:** JSON Schema parse; reject hallucinated ids; **at most one** repair retry per chunk, then abort.

### Stage B — Groq pulse drafting

- **Input:** Merged Stage A JSON + **full text** for reviews in `evidence_review_ids` (join against normalized CSV); keep evidence id lists bounded per theme if needed to limit tokens.
- **Pacing:** **≥60s** after the last Stage A request when TPM pacing requires it.
- **Output:** Structured JSON — **`pulse_body`** (≤250 words), **`quotes[]`** with provenance ids, **`actions[]`** (exactly 3).
- **Validation / retry:** Word count; schema; id existence; PII scan; **at most one** repair retry.

### Deterministic validation layer (before MCP)

| Gate | Description |
|------|-------------|
| Schema | Stage A and Stage B outputs match agreed JSON Schema / pydantic models |
| Quote provenance | Each quote references ≥1 known `review_id`; optional light text overlap check on paraphrases |
| Word limit | `pulse_body` ≤ 250 words |
| PII scan | Block obvious emails, phones, `@handles`, etc. |

### Pre-flight estimator (Phase 3)

Before the first Groq call, compute cumulative planned tokens; **abort or tighten** sampling/truncation if the plan would exceed **100k TPD** or violate **12k TPM** without adequate **≥60s** spacing.

---

## 10. Fallback — chunk-and-merge (not default)

Use when sampling + truncation still cannot fit a safe **per-request** payload, or Stage A JSON fails validation after **at most one** retry per chunk ([architecture §5.7](../../architecture.md)).

| Step | Behavior |
|------|----------|
| 1. Partition | Split **sampled** reviews into chunks each under the **~9k input-token** Stage A budget (§8) |
| 2. Stage A per chunk | One Groq request per chunk; **≥60s** between requests |
| 3. Merge | **Deterministic** dedupe + union `evidence_review_ids` + re-rank; optional small Groq merge only if needed |
| 4. Stage B | Unchanged; **≥60s** after last Stage A call when pacing requires |
| Retries | **Single** repair attempt per chunk — no unbounded retry loops |

With **≤1,000** truncated reviews and conservative chunk sizes, a weekly run should remain within **100k TPD** and **1k RPD** without entering fallback; fallback is for edge cases (aggressive caps, validation failures, or underestimated token mass).

---

## 11. Prompt skeletons (split)

Full system prompts (frozen for Phase 3):

| Stage | Prompt file | JSON Schema |
|-------|-------------|-------------|
| A | [prompts/stage_a_system.md](./prompts/stage_a_system.md) | [schemas/stage_a_output.schema.json](./schemas/stage_a_output.schema.json) |
| B | [prompts/stage_b_system.md](./prompts/stage_b_system.md) | [schemas/stage_b_output.schema.json](./schemas/stage_b_output.schema.json) |

**Essentials (see files for full text):**

- **Stage A:** JSON-only; inject `corpus_stats.json` + sampled reviews; `evidence_review_ids` ⊆ allowed id list; ≤5 themes.
- **Stage B:** JSON-only; merged Stage A + full evidence texts; top 3 themes in `pulse_body`; exactly 3 quotes and 3 actions; ≤250 words.

---

## 12. Summary — Phase 3 readiness

- Corpus statistics (§§1–7) ground Stage A prompts; Stage 0 caps at **≤1,000** reviews with negative-heavy stratification (§9).
- Groq planning follows **`llama-3.3-70b-versatile`** quotas: **30 RPM**, **1k RPD**, **12k TPM**, **100k TPD** — **~9k input tokens** per request, **≥60s** pacing, **deterministic chunk merge**, **single retry** per chunk/stage (§8).
- Default path: **N** Stage A chunk(s) + **one** Stage B + validation; token math in §8 must pass pre-flight before any Groq call.
- Chunk-and-merge (§10) is **fallback only** when per-request budgets or validation still fail after bounded retries.

**Phase 2 artifacts:**

| Artifact | Location |
|----------|----------|
| Stage 0 spec | [stage-0-spec.md](./stage-0-spec.md) |
| Validation rules | [validation-checklist.md](./validation-checklist.md) |
| Sample manifest (generated) | `data/working/sample_manifest.json` |
| Corpus stats (generated) | `data/working/corpus_stats.json` |
| Pre-flight estimate (generated) | `data/working/preflight_estimate.json` |

Phase 3 implements paced Groq A/B, chunk merge, and the validation layer per [implementation plan](../../implementationplan.md) Phase 3 and [architecture §6.1](../../architecture.md). Stage 0 is implemented in `scripts/stage0_sample.py`.
