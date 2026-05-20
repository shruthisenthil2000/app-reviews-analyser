# Agent instructions: Weekly App Review Pulse — Groww

**Target product:** [Groww](https://play.google.com/store/apps/details?id=com.nextbillion.groww) (`com.nextbillion.groww`)
**Store:** Google Play Store only.

This project builds an AI-assisted **weekly pulse** from **public** Play Store reviews for Groww, then delivers it via **MCP-connected Gmail** (draft) and optionally **Google Docs**—not via Google API client code in this repository.

## Non-negotiables (from problem statement)

- **Sources:** Public Play Store reviews only. No scraping behind logins; no private store APIs for ingest.
- **Window:** Last **8–12 weeks** of reviews (convention documented in Phase 2).
- **Themes:** At most **5** themes internally; pulse surfaces **top 3**.
- **Pulse body:** **≤250 words**, scannable; include **3** user quotes (anonymized or paraphrased) and **3** action ideas.
- **PII:** No usernames, emails, or IDs in any artifact, draft, doc, or committed sample.
- **Google integration:** Use **Gmail MCP** and **Google Docs MCP** (or an approved combined Workspace MCP) for drafts and docs. Do **not** add `googleapis` or custom OAuth flows in application code for Gmail/Docs.

## Repository layout (where things go)

| Path | Purpose |
|------|---------|
| `inputs/raw/` | Groww Play Store review CSV for weekly runs (ignored by git by default). |
| `data/working/` | Intermediate normalized datasets (ignored by git). |
| `artifacts/` | Optional on-disk copies of composed pulse text before MCP delivery (ignored by git). |
| `docs/` | Problem statement, architecture, implementation plan, decisions, phase evals. |
| `docs/phases/phase-0X/` | Phase README, checklists, and `eval.md` exit criteria. |
| `runs/phase-0X/` | Optional per-phase scratch (redacted notes only if committed). |
| `scripts/` | Automation that does not embed Google credentials (e.g., secrets hygiene scan). |

## Weekly run (high level)

1. **Orient:** Confirm Groww as the product, week label, and path to `inputs/raw/groww_playstore_reviews.csv`.
2. **Ingest (Phase 2+):** Validate, filter dates, dedupe, normalize—see architecture ingest layer.
3. **Synthesize (Phase 3+):** Themes, quotes (redacted), actions, compose ≤250 words.
4. **Deliver (Phase 4+):** Create Gmail draft via MCP; optional Doc update via MCP.
5. **Verify:** Checklists in `docs/phases/phase-03/eval.md` and `docs/phases/phase-04/eval.md` as those phases complete.

## Phase 1 focus

Before relying on data pipelines, complete **MCP wiring** and **secrets hygiene**. Use:

- `docs/phases/phase-01/mcp-capability-inventory.md` — fill tool capabilities after servers are configured in Cursor.
- `docs/phases/phase-01/smoke-checklist.md` — operator steps for T1.1–T1.3.
- `scripts/check-secrets.sh` — quick repo scan for obvious secret patterns.
- `scripts/fetch_playstore_reviews.py` — fetch public Groww Play Store reviews into `inputs/raw/`.
- `scripts/corpus_stats.py` — deterministic statistics → `data/working/corpus_stats.json`.
- `scripts/stage0_sample.py` — Stage 0 stratified sample (≤1,000) → `data/working/sample_manifest.json`.
- `scripts/preflight_tokens.py` — Groq TPD pre-flight before LLM calls (Phase 3).
- `scripts/run_phase3.py` — Phase 3 pipeline + validation + MCP handoff artifact.
- `scripts/validate_pulse.py` — validate `stage_a_merged.json` / `stage_b_output.json`.
- `scripts/run_phase4.py` — deliver pulse via Saksham MCP (`PULSE_TO_EMAIL`, `GOOGLE_DOC_ID` in `.env`).

## Secrets

- Store API keys in **`.env`** (git-ignored); copy from **`.env.example`**.
- **`GROQ_API_KEY`** — Groq inference for Phase 3+.
- Never commit `.env`, `credentials.json`, or tokens.

## References

- [docs/problemstatement.md](docs/problemstatement.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/implementationplan.md](docs/implementationplan.md)
- [docs/decision.md](docs/decision.md)
