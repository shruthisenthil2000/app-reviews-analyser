# Validation checklist (pre-MCP gate)

**Applies after:** Groq Stage B  
**Blocks:** Gmail / Docs MCP calls on failure  
**Schemas:** [stage_a_output.schema.json](./schemas/stage_a_output.schema.json), [stage_b_output.schema.json](./schemas/stage_b_output.schema.json)  
**Architecture:** [architecture.md](../../architecture.md) §5.6

Phase 3 implements these checks in code; Phase 2 freezes the rules.

---

## 1. JSON schema

| Check | Stage A | Stage B |
|-------|---------|---------|
| Valid JSON parse | Required | Required |
| Matches JSON Schema | [stage_a_output.schema.json](./schemas/stage_a_output.schema.json) | [stage_b_output.schema.json](./schemas/stage_b_output.schema.json) |
| No markdown fences in model output | Strip/reject if present before parse | Same |

**Fail action:** One repair retry per chunk (Stage A) or stage (Stage B); then abort run.

---

## 2. Review ID existence

| Rule | Implementation hint |
|------|---------------------|
| Every `evidence_review_ids[]` entry ∈ normalized CSV | Build `Set[review_id]` from `inputs/raw/groww_playstore_reviews.csv` |
| Every `quotes[].review_ids[]` entry ∈ normalized CSV | Same set |
| Prefer ⊆ sampled ids for Stage A evidence | Warn if id valid in CSV but not in Stage 0 manifest |

**Fail action:** Reject output; optional single Stage A/B retry with explicit id list in prompt.

---

## 3. Quote provenance

| Rule | Detail |
|------|--------|
| Each quote cites ≥1 `review_id` | Schema enforces `review_ids` array |
| Paraphrase allowed | No verbatim usernames; no author fields |
| Optional overlap check | After paraphrase, require minimal token overlap between quote text and joined source review texts (Phase 3: simple word-set Jaccard ≥ 0.15 or substring of significant token) |

**Fail action:** Reject; retry Stage B once with “ground quotes in cited review text” instruction.

---

## 4. Word limit (`pulse_body`)

| Rule | Detail |
|------|--------|
| Maximum | **250 words** (whitespace split acceptable per problem statement) |
| Minimum | Schema minimum length only; no hard minimum word count beyond schema |

**Fail action:** Reject; retry Stage B once; optional deterministic trim only if product owner approves (default: reject).

---

## 5. PII scan (outbound text)

Scan **`pulse_body`**, all **`quotes[].text`**, and **`actions`** string fields.

| Pattern | Example | Action |
|---------|---------|--------|
| Email | `user@domain.com` | Reject or redact `[email]` |
| Phone (10+ digits) | Indian mobile patterns | Reject or redact |
| `@handle` | `@username` | Reject or redact |
| UUID-like Play identifiers in prose | Rare in normalized fetch | Reject if detected |

**Do not scan for:** product name “Groww” in prose.

**Fail action:** Reject; do not call MCP.

---

## 6. Pulse content rules (deterministic, post-schema)

| Rule | Detail |
|------|--------|
| Themes in prose | Top **3** themes reflected in `pulse_body` (Stage A may list up to 5; pulse surfaces 3) |
| Quote count | Exactly **3** quotes (schema) |
| Action count | Exactly **3** actions (schema) |
| No PII in committed artifacts | Redact before saving under `runs/` or `artifacts/` |

---

## 7. Groq quota guards (Phase 3 runtime)

| Guard | Threshold |
|-------|-----------|
| Pre-flight TPD estimate | Abort if planned tokens **≥ 100,000** without tightening sampling |
| Per-request input (Stage A) | Target **≤ ~9,000** tokens before call |
| Pacing | **≥ 60s** between Groq HTTP requests in one run (default) |
| Retries | **≤ 1** repair per chunk / stage |

---

## Operator sign-off (Phase 2 freeze)

- [ ] Schemas reviewed and versioned under `docs/phases/phase-02/schemas/`
- [ ] Stage 0 manifest path agreed: `data/working/sample_manifest.json`
- [ ] PII regex list sufficient for Play review text (no author names in CSV)
