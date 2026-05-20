# Decision Log

This log records **major technical and logical decisions** made while shaping this project’s documentation and delivery approach—including choices introduced when drafting [problemstatement.md](./problemstatement.md), [architecture.md](./architecture.md), [implementationplan.md](./implementationplan.md), and the phase evaluation structure. Routine wording edits are omitted.

**Convention:** Newest decisions first. Status reflects the documentation baseline unless superseded later by the team.

---

## How to use going forward

- Add a row when a choice materially affects scope, security, integrations, or how work is sequenced.
- Prefer **accepted** once the team agrees; use **superseded** with a pointer to the replacing decision ID.

---

| ID | Date | Status | Decision | Context / alternatives |
|----|------|--------|-----------|-------------------------|
| DEC-026 | 2026-05-18 | accepted | **Phase 4 MCP delivery** via Saksham HTTP API ([server](https://saksham-mcp-server-production-f2a5.up.railway.app/)): `POST /create_email_draft` to **`PULSE_TO_EMAIL`** in `.env`, `POST /append_to_doc` to **`GOOGLE_DOC_ID`**. Entry: `scripts/run_phase4.py`. Draft-first (no auto-send). Docs optional if Doc ID unset. | In-repo `googleapis` rejected (DEC-003). Gmail tool: [gmail_tool.py](https://github.com/shruthisenthil2000/shruthi-mcp-server/blob/main/gmail_tool.py). |
| DEC-025 | 2026-05-18 | accepted | **Phase 3 pipeline** in `scripts/run_phase3.py`: Groq A/B via `run_weekly_pulse.py`, deterministic validation (`validate_pulse.py`), finalize to `runs/phase-03/` + `artifacts/mcp_delivery.json`. Phase 4 MCP documented for [Saksham Google MCP server](https://saksham-mcp-server-production-f2a5.up.railway.app/) (`create_email_draft`, `append_to_doc`). | Groq calls stay in repo scripts; Gmail/Docs only via MCP per DEC-003. |
| DEC-024 | 2026-05-17 | accepted | **Groq quota-aware planning** for `llama-3.3-70b-versatile`: **30 RPM**, **1k RPD**, **12k TPM**, **100k TPD**. Stage 0 hard cap **≤1,000** reviews; Stage A target **~9k input tokens** per request with **≥60s** pacing; **deterministic chunk merge** preferred; **≤1** JSON repair retry per chunk/stage. Pre-flight estimator in `scripts/preflight_tokens.py`. | Alternative: send full ~64k-token corpus in one call. **Rejected** — violates TPM/TPD and DEC-023 sampling goals. Documented in architecture §6.1, Phase 2 schemas/prompts, and `docs/phases/phase-02/stage-0-spec.md`. |
| DEC-023 | 2026-05-17 | accepted | **Production-style Groq pipeline:** **Stage 0** deterministic stratified sampling (rating tier × ISO week, seed-fixed, negative-priority caps) → **Stage A** theme discovery (JSON-only, themes + `evidence_review_ids`) → **Stage B** concise pulse (quotes + actions, ≤250 words, structured JSON) → **deterministic validation** (schema, provenance, word limit, PII). **Chunk-and-merge** remains fallback only (architecture §5.7). | Supersedes single-pass full corpus (DEC-022). Alternative single-pass rejected for production alignment: reduces token noise, improves reproducibility, and narrows Stage B context to provenance-grounded reviews only. |
| DEC-022 | 2026-05-17 | superseded | ~~Single-pass full-corpus prompting~~ | Superseded by **DEC-023** (stratified sampling + two-stage Groq + validation). Chunk-and-merge retained as fallback. |
| DEC-021 | 2026-05-17 | accepted | **Inject pre-LLM deterministic statistics** (rating distribution, 8 keyword-based topic clusters, top bigrams) into Groq prompts for grounding | Alternative: let the LLM discover everything from raw text alone. **Rejected** because grounding reduces hallucination risk and lets the LLM reference concrete numbers (e.g., "40% of reviews mention trading") rather than guessing. Stats feed **Stage A** (and optionally Stage B). |
| DEC-020 | 2026-05-17 | accepted | **Groq** as LLM inference provider; primary model `llama-3.3-70b-versatile` | Alternatives: OpenAI GPT-4o (cost), local models (ops burden). **Chosen** Groq for fast inference. Effective limits for planning are **TPM/TPD/RPM/RPD** (DEC-024), not single large-context dumps — sampled + chunked Stage A and evidence-only Stage B. |
| DEC-019 | 2026-05-15 | accepted | **Normalize at fetch time:** drop reviews with <=6 words, containing emojis, or containing non-English scripts | Alternative: keep all reviews and filter later in Phase 2/3. **Rejected** — filtering at source keeps `inputs/raw/` clean and avoids carrying noise into analysis. Reduces 12,049 raw rows to 2,110 high-quality English reviews across 13 weeks. |
| DEC-018 | 2026-05-15 | accepted | **Target product is Groww** (`com.nextbillion.groww`), **Play Store only** — App Store ingestion removed | Alternative: dual-store (App Store + Play). **Rejected** — user directive to focus on Groww Play Store data only. iTunes RSS fetcher and App Store sample data deleted. |
| DEC-017 | 2026-05-15 | accepted | **Fetch Groww reviews via `google-play-scraper`** (`scripts/fetch_playstore_reviews.py`), which reads publicly visible Play Store pages without login | Alternative: Play Console export (requires developer login — out of scope per DEC-002). Bright Data MCP scraper (auth issue in current env). Chosen `google-play-scraper` library for reliability and public-data posture. Author names are **not** written to CSV. |
| DEC-016 | 2026-05-15 | superseded | ~~Multi-country App Store RSS sweep~~ | Superseded by DEC-018 (Groww, Play Store only). |
| DEC-015 | 2026-05-15 | superseded | ~~Optional App Store bootstrap via iTunes RSS~~ | Superseded by DEC-018 (Groww, Play Store only). |
| DEC-013 | 2026-05-14 | accepted | **Repository folder layout** for Phase 1: `inputs/raw/`, `data/working/`, `artifacts/`, `docs/phases/phase-0X/`, `runs/phase-0X/`, root `AGENTS.md` and `scripts/check-secrets.sh` | Alternative: single flat `data/` folder or phase-specific input dirs under `runs/`. **Chosen** split so exports, derived data, and optional composed files are clearly separated; `runs/phase-XX` gives a dedicated scratch area without mixing eval docs. |
| DEC-012 | 2026-05-14 | accepted | Document the system as **five sequential phases** with explicit evaluation gates | Alternative: fewer combined phases (faster on paper) or more granular phases (per store, per MCP server). **Rejected** fewer phases to avoid mixing MCP setup with narrative quality gates; **rejected** finer fragmentation to keep milestone overhead reasonable for a course-scale project. |
| DEC-011 | 2026-05-14 | accepted | **Block formal Phase 4 completion** on Phase 3 exit criteria | Alternative: deliver drafts early to “see something in Gmail” while themes are still unstable. **Rejected** to reduce risk of sharing non-compliant or misleading pulses; light Phase 4 experimentation with dummy text is still compatible with the implementation plan wording. |
| DEC-010 | 2026-05-14 | accepted | **Allow partial overlap** of Phase 2 and Phase 3 once Phase 1 MCP stability is minimally proven | Alternative: strict waterfall with no analysis until ingest is “perfect.” **Rejected** to preserve momentum; overlap requires clear fixtures so ingest quality does not silently poison early narratives. |
| DEC-009 | 2026-05-14 | accepted | Keep **one consolidated `decision.md`** rather than scattering decisions only inside architecture or phase evals | Alternative: per-phase decision files. **Rejected** to give auditors and teammates a single index of major choices; phase evals still hold test and exit detail only. |
| DEC-008 | 2026-05-14 | accepted | Place per-phase quality material in **`docs/phases/phase-XX/eval.md`** | Alternative: a single `eval.md` for all phases or naming like `phase-1-eval.md` at `docs/` root. **Rejected** in favor of one folder per phase so future artifacts (screenshots, notes) can sit beside `eval.md` without cluttering top-level docs. |
| DEC-007 | 2026-05-14 | accepted | Treat **Gmail output as draft-first** as the default product posture | Alternative: auto-send for convenience. **Rejected** for milestone safety and reviewability; can be revisited via a new decision if course or org policy requires send. |
| DEC-006 | 2026-05-14 | accepted | Treat **Google Docs as optional** at the architecture level while still requiring MCP (not raw APIs) when Docs is used | Alternative: mandate a running Doc for every run. **Rejected** as a universal requirement because MCP capability sets vary; milestone text allows optional Doc when the chosen server supports it—record waiver in Phase 4 eval if Docs is skipped. |
| DEC-005 | 2026-05-14 | accepted | Define architecture using **layers** (ingest, analysis, compose, deliver) plus **distinct agent roles** across the weekly run | Alternative: single “black box agent does everything” description. **Rejected** because separation improves test planning, clarifies where MCP plugs in, and matches how operators debug failures. |
| DEC-004 | 2026-05-14 | accepted | Use **Mermaid** for system and weekly sequence views in architecture | Alternative: text-only diagrams or external diagram files. **Chosen** Mermaid for versionability and easy editing in-repo alongside Markdown. |
| DEC-003 | 2026-05-14 | accepted | Position **MCP as the sole integration path for Gmail and Google Docs** in this milestone; no parallel Google API clients in application code for those surfaces | Alternative: implement OAuth and REST in-repo for richer control. **Rejected** to align with the problem statement’s integration constraint and to concentrate credential handling in the MCP host. |
| DEC-002 | 2026-05-14 | accepted | Restrict review sourcing to **public exports only** (no authenticated scraping) | Alternative: private APIs or scraping behind logins for completeness. **Rejected** for compliance and scope fit with the stated milestone constraints. |
| DEC-001 | 2026-05-14 | accepted | Anchor documentation in **Cursor as the primary MCP-capable agent host** while wording remains host-agnostic enough to substitute another MCP-aware environment | Alternative: specify no host. **Rejected** vague host; the course context assumes Cursor-class tooling for MCP. |

---

## Template for new decisions

Add a new row above the template block (newest first).

```text
| DEC-024 | YYYY-MM-DD | accepted | Short title | Alternatives considered and why rejected or deferred |
```
