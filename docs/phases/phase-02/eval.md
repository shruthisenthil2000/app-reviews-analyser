# Phase 2 -- Evaluation: Data analysis and LLM strategy

## Scope

Validate that the Groww review corpus has been profiled, the Groq **multi-stage** pipeline is specified (Stage 0 → Stage A → Stage B → validation), and Phase 3 can implement against frozen contracts.

## Testing

| ID | Test | How to run | Expected |
|----|------|------------|----------|
| T2.1 | Corpus profile complete | Check [data-analysis.md](./data-analysis.md) §§1–7 | Rating distribution, weekly trends, topic prevalence documented |
| T2.2 | Normalization validation | Re-run fetch script; compare row count and date span | Consistent with Phase 1 run log (minor variance acceptable) |
| T2.3 | Token rationale | Check [data-analysis.md](./data-analysis.md) §8 and `data/working/preflight_estimate.json` | ≤1,000 sample cap, ~9k/request target, Groq TPM/TPD limits; pre-flight passes |
| T2.4 | Groq model selected | Check [decision.md](../../decision.md) | Model name, context window, rationale (DEC-020 / DEC-023) |
| T2.5 | Primary pipeline specified | Check [data-analysis.md](./data-analysis.md) §9 | Stage 0 buckets (tier × ISO week), seed, caps, Stage A JSON + evidence ids, Stage B pulse + provenance |
| T2.6 | Fallback documented | Check [data-analysis.md](./data-analysis.md) §10 | Chunk-and-merge triggers and merge behavior described |
| T2.7 | Prompt skeletons | Check [prompts/](./prompts/) and [data-analysis.md](./data-analysis.md) §11 | Full Stage A and Stage B system prompts |
| T2.8 | Validation gates | Check [architecture.md](../../architecture.md) §5.6 | Schema, id existence, provenance, ≤250 words, PII scan |

## Exit criteria (all must pass)

- [x] [data-analysis.md](./data-analysis.md) complete through §12.
- [x] **DEC-023** and **DEC-024** in [decision.md](../../decision.md).
- [x] Stage 0 spec + manifest: [stage-0-spec.md](./stage-0-spec.md), `data/working/sample_manifest.json`.
- [x] Stage A/B JSON schemas under [schemas/](./schemas/).
- [x] [validation-checklist.md](./validation-checklist.md) covers schema, ids, provenance, ≤250 words, PII, quotas.
- [x] [prompts/stage_a_system.md](./prompts/stage_a_system.md) and [prompts/stage_b_system.md](./prompts/stage_b_system.md).
- [x] Chunk-and-merge documented **only** as fallback (data-analysis §10, architecture §5.7).
- [x] Topic landscape mapped — keyword clusters with counts (data-analysis §4).
- [x] Deterministic scripts run — see [PHASE2-RUN-LOG.md](../../../runs/phase-02/PHASE2-RUN-LOG.md).

## Evidence to attach at phase close

- [data-analysis.md](./data-analysis.md), [stage-0-spec.md](./stage-0-spec.md), [validation-checklist.md](./validation-checklist.md)
- [PHASE2-RUN-LOG.md](../../../runs/phase-02/PHASE2-RUN-LOG.md)
- Decision log: DEC-020, DEC-021, DEC-023, DEC-024
