# Golden pulse acceptance notes (Phase 3 regression)

**Fixture sources:** `data/working/stage_a_merged.json`, `stage_b_output.json` from a Groww weekly run.

## Expected structure (T3.1–T3.4)

- Stage A: **≤5** themes with `label`, `summary`, `evidence_review_ids`.
- Stage B: `pulse_body` **≤250 words**; exactly **3** quotes; exactly **3** actions.
- Top **3** themes reflected in `pulse_body` prose.

## Theme labels (illustrative — not exact match required)

Accept any merge that clearly covers:

1. Brokerage / fees / charges
2. Customer support responsiveness
3. Withdrawals, payments, or selling friction
4. App stability / technical glitches (optional 4th–5th theme)

## PII (T3.5)

- No emails, phone numbers, or `@handles` in outbound pulse text.
- Quotes may paraphrase storefront language; avoid pasting long verbatim PII.

## Validation command

```bash
python3 scripts/validate_pulse.py
```

Must exit **0** before Phase 4 MCP delivery.
