# Phase 5 — Evaluation: Integration, quality gates, and operations

## Scope

End-to-end weekly run from exports through pulse to MCP delivery, with documentation and repeatable checks suitable for milestone demo.

## Testing

| ID | Test | How to run | Expected |
|----|------|------------|----------|
| T5.1 | E2E dry run | Follow runbook using fixture or anonymized exports | Completes without manual code edits mid-run |
| T5.2 | Phase regression | Re-run key checks from [phase-01](./phase-01/eval.md), [phase-02](./phase-02/eval.md), [phase-03](./phase-03/eval.md), [phase-04](./phase-04/eval.md) | All prior exit criteria still pass |
| T5.3 | Runbook accuracy | Have someone not on core implementation follow runbook | ≤N clarifying questions (set N to 3); update doc if exceeded |
| T5.4 | Failure modes | Document MCP auth expiry or quota errors | Clear recovery steps in runbook |
| T5.5 | Demo path | Record checklist for milestone demo | Covers ingest → pulse → draft in ≤15 minutes wall time |

## Exit criteria (all must pass)

- [ ] A weekly runbook exists (`docs/runbook.md` or an equivalent section linked from [implementationplan.md](../../implementationplan.md)) and describes weekly execution end-to-end.
- [ ] T5.1 and T5.2 pass; gaps filed as issues with owners or deferred via [decision.md](../../decision.md).
- [ ] Stakeholder-facing summary (1 paragraph) explains who the pulse helps and how to consume it.
- [ ] Repository is demo-ready: no secrets, no PII in samples, architecture diagram current.

## Evidence to attach at phase close

- Link to runbook and demo checklist.
- Optional: short screen recording or transcript of E2E run (redacted).
