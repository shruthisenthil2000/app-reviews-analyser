#!/usr/bin/env python3
"""
Pre-flight token estimator for Groq quota planning (Phase 2 spec / Phase 3 runtime).

Reads:  data/working/sampled_reviews.json, data/working/corpus_stats.json
Writes: data/working/preflight_estimate.json

Usage:
  python3 scripts/stage0_sample.py && python3 scripts/corpus_stats.py && python3 scripts/preflight_tokens.py
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Architecture §6.1 defaults
INPUT_TOKEN_TARGET = 9000
TPD_LIMIT = 100_000
STAGE_B_PLAN_TOKENS = 15_000
RETRY_HEADROOM = 5_000
PROMPT_OVERHEAD_PER_CHUNK = 1200


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate Groq token usage for a weekly run.")
    parser.add_argument("--sample", type=Path, default=ROOT / "data/working/sampled_reviews.json")
    parser.add_argument("--stats", type=Path, default=ROOT / "data/working/corpus_stats.json")
    parser.add_argument("--out", type=Path, default=ROOT / "data/working/preflight_estimate.json")
    parser.add_argument("--input-target", type=int, default=INPUT_TOKEN_TARGET)
    args = parser.parse_args()

    for path in (args.sample, args.stats):
        if not path.is_file():
            print(f"ERROR: missing {path} — run stage0_sample.py and corpus_stats.py first", file=sys.stderr)
            return 1

    sample = json.loads(args.sample.read_text(encoding="utf-8"))
    stats = json.loads(args.stats.read_text(encoding="utf-8"))

    trunc_words = sum(len(r.get("text_truncated", "").split()) for r in sample)
    review_tokens = int(trunc_words * 1.3)
    stats_tokens = min(2500, int(len(json.dumps(stats)) / 4))

    per_chunk_review_budget = max(500, args.input_target - PROMPT_OVERHEAD_PER_CHUNK - stats_tokens)
    n_chunks = max(1, math.ceil(review_tokens / per_chunk_review_budget))
    stage_a_tokens = n_chunks * args.input_target
    planned_total = stage_a_tokens + STAGE_B_PLAN_TOKENS + RETRY_HEADROOM
    within_tpd = planned_total < TPD_LIMIT

    result = {
        "schema_version": "1.0",
        "sampled_reviews": len(sample),
        "truncated_review_tokens_est": review_tokens,
        "stats_block_tokens_est": stats_tokens,
        "input_token_target_per_request": args.input_target,
        "estimated_stage_a_chunks": n_chunks,
        "estimated_stage_a_tokens": stage_a_tokens,
        "estimated_stage_b_tokens": STAGE_B_PLAN_TOKENS,
        "retry_headroom": RETRY_HEADROOM,
        "planned_daily_tokens": planned_total,
        "tpd_limit": TPD_LIMIT,
        "within_tpd": within_tpd,
        "pacing_seconds_between_requests": 60,
        "groq_model": "llama-3.3-70b-versatile",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    status = "OK" if within_tpd else "OVER_TPD"
    print(f"Wrote {args.out} — {status} (planned {planned_total} / {TPD_LIMIT} TPD, {n_chunks} Stage A chunk(s))")
    return 0 if within_tpd else 2


if __name__ == "__main__":
    raise SystemExit(main())
