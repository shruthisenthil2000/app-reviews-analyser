# Phase 3 — Evaluation: Analysis and pulse generation

## Scope

Validate theme grouping (≤5 internal, top 3 in pulse), quote selection, action ideas, word limit, and PII-free output.

## Testing

| ID | Test | How to run | Expected |
|----|------|------------|----------|
| T3.1 | Theme cap | Run on fixture with diverse topics | At most 5 themes; pulse shows top 3 |
| T3.2 | Quote count | Inspect generated pulse | Exactly 3 quotes (or 3 paraphrases) aligned to themes |
| T3.3 | Actions | Inspect generated pulse | Exactly 3 action ideas, concrete and tied to themes |
| T3.4 | Word count | Count words in pulse body (exclude optional metadata headers if excluded by convention) | ≤250 words |
| T3.5 | PII scan | Manual + simple grep for email-like patterns, @handles, “user123” style IDs | No matches; redaction rules documented |
| T3.6 | Readability | Stakeholder skim (self or peer) | Understandable in under one minute |

## Exit criteria (all must pass)

- [x] Pulse structure matches problem statement: top 3 themes, 3 quotes, 3 actions (`scripts/validate_pulse.py`).
- [x] Word count and theme constraints enforced (`pulse_body` ≤250 words; ≤5 themes in Stage A).
- [x] PII regex scan in `pipeline/validate_output.py`; quotes use paraphrase + provenance overlap check.
- [x] Golden acceptance notes: [fixtures/pulse/golden_acceptance.md](../../../fixtures/pulse/golden_acceptance.md).

**Validate:** `python3 scripts/validate_pulse.py` → exit 0.

## Evidence to attach at phase close

- Sanitized example pulse (paste or file).
- Record of word count and theme list for that example.
