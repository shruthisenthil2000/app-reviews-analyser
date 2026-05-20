# Phase-Wise Implementation Plan

This plan implements the weekly review pulse for **Groww** (`com.nextbillion.groww`, Play Store only) using **Groq** for LLM inference and **MCP** for Gmail/Google Docs delivery. It is aligned with [problemstatement.md](./problemstatement.md) and [architecture.md](./architecture.md).

---

## Document map

| Artifact | Role |
|----------|------|
| [architecture.md](./architecture.md) | Stable mental model: components, boundaries, flows, Groq integration |
| This file | Sequenced work across phases |
| [phases/phase-XX/eval.md](./phases/phase-01/eval.md) | Per-phase testing and exit criteria |
| [decision.md](./decision.md) | Major technical and logical choices |

---

## Repository layout (Phase 1)

| Path | Purpose |
|------|---------|
| [README.md](../README.md) | Project entry and tree overview |
| [AGENTS.md](../AGENTS.md) | Agent constraints and weekly run summary |
| `inputs/raw/` | Groww Play Store review CSV ([inputs/README.md](../inputs/README.md)); git-ignored |
| `data/working/` | Intermediate normalized datasets; git-ignored |
| `artifacts/` | Optional local composed pulse copies; git-ignored |
| `docs/phases/phase-0X/` | Phase `README.md`, `eval.md`, and Phase 1 checklists |
| `runs/phase-0X/` | Optional scratch per phase (redacted notes only if committed) |
| [scripts/check-secrets.sh](../scripts/check-secrets.sh) | Phase 1 T1.4 helper |
| [scripts/fetch_playstore_reviews.py](../scripts/fetch_playstore_reviews.py) | Fetch and normalize public Groww Play Store reviews |

---

## Phase overview

| Phase | Name | Primary outcome |
|-------|------|-----------------|
| 1 | Foundation and MCP wiring | Environment ready; normalized Groww corpus fetched; MCP servers configured |
| 2 | Data analysis and LLM strategy | Corpus profiled; **Stage 0** stratified sampling rules + caps documented; **Stage A/B** prompt schemas fixed |
| 3 | Groq-powered pulse generation | Working pipeline: Stage A theme JSON → Stage B pulse → **deterministic validation** → artifact ≤250 words |
| 4 | MCP delivery | Pulse reaches Gmail (and optionally Docs) only through MCP |
| 5 | Integration, quality gates, and operations | End-to-end weekly run is repeatable and demo-ready |

**Dependency rule:** Phase 4 must not be treated as complete until Phase 3 exit criteria are satisfied. Phase 2 can overlap with Phase 1 once the corpus is fetched.

---

## Phase 1 -- Foundation and MCP wiring

### Intent

Establish the execution home for the agent and the contract with Google Workspace through MCP. Fetch and normalize the Groww review corpus.

### Scope in

- Cursor as the MCP host; Gmail MCP and Google Docs MCP configuration.
- Fetch script (`scripts/fetch_playstore_reviews.py`) for Groww Play Store reviews.
- Normalization rules: >6 words, no emojis, English only, deduplication, 12-week window.
- Repository layout, secrets hygiene, agent guidance artifacts.

### Scope out

- Theme taxonomy (Phase 2/3).
- LLM model selection (Phase 2).
- Production scheduling.

### Deliverables

- Normalized corpus: `inputs/raw/groww_playstore_reviews.csv` (2,110 reviews, 13 ISO weeks).
- MCP capability inventory and smoke checklist.
- Secrets scan passing.

**Evaluation:** [phases/phase-01/eval.md](./phases/phase-01/eval.md)

---

## Phase 2 -- Data analysis and LLM strategy

### Intent

With the normalized corpus from Phase 1 in hand (~2,100+ Groww Play Store reviews in a typical window), Phase 2 analyzes the data and locks in a **quota-aware Groq pipeline**: **deterministic statistics → Stage 0 stratified sampling (hard cap ≤1,000 reviews for LLM-bound stages) → Groq Stage A (themes + evidence ids; chunked if needed) → deterministic merge when possible → Groq Stage B (pulse)**. **Chunk-and-merge** remains documented only as fallback when sampling + truncation still exceed safe **per-request** size or validation fails after bounded retries (see [architecture.md §6.1](./architecture.md)).

### Scope in

- **Corpus profiling:** Rating distribution, weekly volume trends, word-length statistics, topic-signal extraction (keyword/bigram frequency) — documented in [data-analysis.md](./phases/phase-02/data-analysis.md).
- **Stage 0 specification:** Stratified buckets (**rating tier × ISO week**), **negative-priority caps**, **deterministic ordering** (e.g. sort by `review_id`), **fixed seed** reproducibility, target sample within **≤1,000 rows** entering Groq (corpus may exceed that — sampling always trims first), manifest artifact under `data/working/`.
- **Groq quotas & pacing:** Document planning against **`llama-3.3-70b-versatile`** limits: **30 RPM**, **1,000 RPD**, **12k TPM**, **100k TPD** — wire defaults into spec: **≥60s** between requests in a single run, **≤~9k input tokens** target per request before Stage A (architecture §6.1), **at most one** JSON repair retry per chunk/stage, prefer **deterministic** chunk merge (no extra Groq merge call).
- **Groq model selection:** Primary model `llama-3.3-70b-versatile` (or successor); confirm **Stage A chunk count × ~9k + Stage B + retry headroom < 100k TPD** under worst-case weekly assumptions.
- **Stage A contract:** JSON-only output schema — themes (≤5) each with `evidence_review_ids` drawn only from sampled ids.
- **Stage B contract:** JSON with `pulse_body`, quotes + provenance ids, actions; ≤250 words enforced downstream by validator.
- **Validation specification:** JSON Schema / field rules, quote provenance checks, word limit, PII scan rules.
- **Fallback:** Chunk-and-merge for Stage A when context limits or repeated validation failures occur.

### Data insights driving strategy (from Phase 1 corpus)

| Insight | Implication |
|---------|-------------|
| ~2,100+ reviews possible in window; negative reviews longer on average | **Hard cap ≤1,000** plus **stratified sampling with negative-heavy caps** preserves pain signals while staying under **TPM/TPD** |
| Bimodal ratings (many 1★ and 5★) | Tiered sampling (negative / neutral / positive) avoids dominance by generic praise |
| Strong weekly variance (77–293 reviews/week) | Per-week buckets prevent a single week from swallowing the quota |
| Eight keyword topic clusters | Inject aggregates into Stage A prompt so themes align with measurable signals |

### Scope out

- Implementing the Groq client and validators end-to-end (Phase 3) — Phase 2 only **specifies** contracts.
- Gmail or Docs operations (Phase 4).

### Workstreams

1. **Corpus profile report:** [docs/phases/phase-02/data-analysis.md](./phases/phase-02/data-analysis.md).
2. **Stage 0 parameters:** Document tier definitions, per-cell caps, seed env var, manifest schema.
3. **JSON schemas:** Stage A output (themes + evidence ids); Stage B output (pulse_body + quotes + actions + provenance).
4. **Validation checklist:** Schema validation, id existence, provenance, word count, PII regex list.
5. **Groq model / fallback:** Record in [decision.md](./decision.md); note chunk-and-merge trigger conditions.
6. **Prompt skeletons:** Separate Stage A and Stage B system prompts (JSON-only for Stage A).

### Checkpoints

- Mid-phase: data-analysis.md updated with pipeline strategy; Stage 0 parameters drafted.
- End-phase: Stage A/B schemas + validation rules approved; ready for Phase 3 implementation.

### Risks

- **Over-aggressive sampling:** Rare themes dropped. Mitigation: raise negative tier caps slightly or run diagnostic keyword pass before sampling.
- **Under-sampling:** Themes lose nuance. Mitigation: tune tier/week caps up to the **1,000** ceiling or lengthen truncation slightly while re-checking §6.1 token math.
- **Quota exhaustion:** Mid-run **429** or daily cap hit. Mitigation: pre-flight token estimator; fewer chunks; shorter truncation; defer remainder to next UTC day only if **TPD** truly exhausted.
- **Groq model deprecation:** Document fallback model IDs.

### Handoff to Phase 3

Deliver: corpus profile, Stage 0 spec, Stage A/B JSON schemas, validation rules, prompt skeletons.

**Evaluation:** [phases/phase-02/eval.md](./phases/phase-02/eval.md)

---

## Phase 3 -- Groq-powered pulse generation (multi-stage)

### Intent

Implement and run the pipeline: **deterministic stats → Stage 0 sample → Groq Stage A → Groq Stage B → validation →** optional artifact export before MCP.

### Scope in

- **Stage 0 implementation:** Deterministic stratified sampler emitting `data/working/sample_manifest.json` + in-memory payload for Groq.
- **Groq Stage A:** Theme discovery — **one HTTP request per chunk** when chunking is required; **parse JSON only**; validate schema; **at most one** repair retry per chunk (protect **RPD/TPD**). **≥60s** delay between successive Groq requests unless telemetry proves a tighter safe interval.
- **Chunk merge:** Prefer **in-process deterministic** consolidation of per-chunk Stage A JSON (dedupe labels, union ids); optional tiny Groq merge only if product requirements demand it and **daily** math still passes.
- **Groq Stage B:** Pulse drafting — typically **one** call using merged Stage A JSON + **full text for evidence ids only** (expand ids → texts from normalized CSV); cap evidence id lists per theme if needed to bound Stage B tokens.
- **Pre-flight estimator:** Before any Groq call, estimate input/output tokens (`≈1.3 × words` + prompt overhead) and **abort or tighten sampling** if cumulative plan would exceed **100k TPD** or blow **12k TPM** in a single minute without pacing.
- **Deterministic validation layer:** Schema validation; **review_id** existence in `inputs/raw/groww_playstore_reviews.csv`; quote provenance mapping; word count ≤250 on `pulse_body`; PII scan.
- **Logging:** Log sampling seed, caps, counts per tier/week, **chunk index/total**, **per-request and cumulative daily** token estimates vs provider-reported usage where available, validation outcomes.

### Scope out

- Gmail or Docs delivery (Phase 4).
- Auto-send without human review.

### Workstreams

1. **Pipeline orchestration script(s):** One command or agent flow chaining Stage 0 → A → B → validation.
2. **Stage A prompt:** Forces JSON-only output; lists allowed `review_id` universe explicitly.
3. **Stage B prompt:** Consumes validated Stage A JSON; requires each quote to cite `review_id`(s).
4. **Validator module:** Pydantic / JSON Schema + regex PII checks + word count.
5. **Golden run:** Save redacted Stage A/B JSON + final pulse under `runs/phase-03/` or `artifacts/`.
6. **Fallback testing:** Dry-run chunk-and-merge path on a trimmed fixture if time permits.

### Checkpoints

- Mid-phase: Stage A JSON reliably validates; evidence ids are non-hallucinated.
- End-phase: End-to-end pulse passes **all** validation gates; ≤250 words; no PII hits.

### Risks

- **Hallucinated evidence ids:** Strict prompt + validator rejection + **single** retry only (quota-aware).
- **Quote drift after paraphrase:** Minimum provenance check per architecture §5.6; tighten Stage B instructions if validation flakes.

### Handoff to Phase 4

Validated plain-text (or MCP-ready) pulse plus structured JSON package.

**Evaluation:** [phases/phase-03/eval.md](./phases/phase-03/eval.md)

---

## Phase 4 -- MCP delivery

### Intent

Make the weekly pulse actionable in Google Workspace using only MCP: Gmail draft to self or alias, and optional Google Doc updates.

### Scope in

- **Gmail:** Draft creation with correct recipient policy, week-labeled subject, and pulse body.
- **Docs (if in scope):** Create or update behavior aligned with Docs MCP capabilities.
- **Failure handling:** Procedures for timeout, permission denied, or quota errors.
- **Proof of path:** No parallel Google API clients in the repo.

### Scope out

- Changing the analytical content of the pulse except for formatting fixes.

### Workstreams

1. **Parameter contract:** Stable mapping from pulse sections to email body and optional Doc structure.
2. **Dry delivery rehearsal:** Deliver placeholder text before using real pulse content.
3. **Operator confirmation:** Human opens Gmail draft and confirms formatting.
4. **Docs policy:** If append is unsupported, pivot to new-doc-per-week or waive.

### Checkpoints

- Mid-phase: Gmail draft path proven.
- End-phase: Docs path proven or formally waived.

### Risks

- **Formatting loss:** Bullets or line breaks collapse. Adjust structure.
- **Permission scope:** MCP account cannot write to intended Doc. Share Doc or use a new one.

### Handoff to Phase 5

Stable happy path plus list of known limitations.

**Evaluation:** [phases/phase-04/eval.md](./phases/phase-04/eval.md)

---

## Phase 5 -- Integration, quality gates, and operations

### Intent

Treat the system as a weekly product: reproducible steps, regression mindset, and demo readiness.

### Scope in

- **End-to-end runbook:** From fetch through pulse generation through MCP delivery through verification.
- **Regression bundle:** Re-check earlier phase exit criteria.
- **Demo narrative:** Why the pulse matters, what data fed it, what changed versus last week.
- **Knowledge transfer:** Another operator can execute the runbook.

### Scope out

- Long-term automation and monitoring (capture as future work).

### Workstreams

1. **Runbook authoring:** Single doc with prerequisites, duration, and troubleshooting.
2. **Weekly cadence definition:** Week start day, late-arriving data handling, subject line naming.
3. **Quality gate checklist:** Consolidated problem statement and phase eval checks.
4. **Retrospective:** What would break in week two of real use.

### Checkpoints

- Mid-phase: Independent walkthrough of runbook with <=3 clarifying questions.
- End-phase: All phase evaluations satisfied or explicitly waived.

### Risks

- **Last-minute scope creep:** Log new ideas as future work, not under this milestone.

### Handoff

Project ready for submission or operational handoff.

**Evaluation:** [phases/phase-05/eval.md](./phases/phase-05/eval.md)

---

## Cross-phase dependencies

```text
Phase 1 ----> Phase 2 ----> Phase 3 ----> Phase 4 ----> Phase 5
    \_____________ partial overlap allowed _____________/
```

**Overlap guidance:** Phase 2 can start once Phase 1 corpus exists. Phase 3 implements Stage 0 + Groq A/B + validation per architecture. Phase 4 delivery experiments should use placeholder text until Phase 3 validation passes.

---

## Related documents

- [Architecture](./architecture.md)
- [Decision log](./decision.md)
