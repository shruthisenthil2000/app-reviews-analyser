#!/usr/bin/env python3
"""
Stage 0: deterministic stratified sampling for the Groww review pulse pipeline.

Reads:  inputs/raw/groww_playstore_reviews.csv (default)
Writes: data/working/sample_manifest.json
        data/working/sampled_reviews.json

Spec: docs/phases/phase-02/stage-0-spec.md

Usage:
  python3 scripts/stage0_sample.py
  SAMPLER_SEED=42 python3 scripts/stage0_sample.py --max-reviews 1000
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import (  # noqa: E402
    ReviewRow,
    estimate_tokens,
    load_dotenv,
    load_reviews_csv,
    stride_subsample,
    truncate_text,
    utc_now_iso,
)

load_dotenv()

TIER_ORDER = ("negative", "neutral", "positive")


def bucket_rows(rows: List[ReviewRow]) -> Dict[Tuple[str, str], List[ReviewRow]]:
    buckets: Dict[Tuple[str, str], List[ReviewRow]] = defaultdict(list)
    for row in rows:
        buckets[(row.iso_week, row.tier)].append(row)
    for key in buckets:
        buckets[key].sort(key=lambda r: r.review_id)
    return buckets


def run_sampling(
    rows: List[ReviewRow],
    *,
    seed: int,
    global_max: int,
    text_max_chars: int,
    tier_caps: Dict[str, int],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    buckets = bucket_rows(rows)
    weeks = sorted({w for w, _ in buckets})
    bucket_summary: List[Dict[str, Any]] = []
    selected_rows: List[ReviewRow] = []
    seen_ids: set[str] = set()

    for week in weeks:
        for tier in TIER_ORDER:
            if len(selected_rows) >= global_max:
                break
            key = (week, tier)
            pool = buckets.get(key, [])
            cap = tier_caps[tier]
            ids = [r.review_id for r in pool]
            picked_ids = stride_subsample(ids, cap)
            remaining = global_max - len(selected_rows)
            if len(picked_ids) > remaining:
                picked_ids = picked_ids[:remaining]

            id_set = set(picked_ids)
            for row in pool:
                if row.review_id in id_set and row.review_id not in seen_ids:
                    selected_rows.append(row)
                    seen_ids.add(row.review_id)

            bucket_summary.append(
                {
                    "iso_week": week,
                    "tier": tier,
                    "pool_size": len(pool),
                    "selected_count": sum(1 for r in selected_rows if r.iso_week == week and r.tier == tier),
                }
            )
        if len(selected_rows) >= global_max:
            break

    # Recompute selected_count per bucket accurately
    counts: Dict[Tuple[str, str], int] = defaultdict(int)
    for row in selected_rows:
        counts[(row.iso_week, row.tier)] += 1
    for entry in bucket_summary:
        entry["selected_count"] = counts[(entry["iso_week"], entry["tier"])]

    manifest_reviews = [
        {
            "review_id": r.review_id,
            "rating": r.rating,
            "date": r.date,
            "iso_week": r.iso_week,
            "tier": r.tier,
        }
        for r in selected_rows
    ]

    sampled_payload = [
        {
            "review_id": r.review_id,
            "rating": r.rating,
            "date": r.date,
            "iso_week": r.iso_week,
            "tier": r.tier,
            "text": r.text,
            "text_truncated": truncate_text(r.text, text_max_chars),
        }
        for r in selected_rows
    ]

    trunc_words = sum(len(r["text_truncated"].split()) for r in sampled_payload)
    manifest: Dict[str, Any] = {
        "schema_version": "1.0",
        "product": "com.nextbillion.groww",
        "source_csv": "inputs/raw/groww_playstore_reviews.csv",
        "created_at": utc_now_iso(),
        "sampler_seed": seed,
        "global_max_reviews": global_max,
        "text_max_chars": text_max_chars,
        "tier_caps": tier_caps,
        "corpus_row_count": len(rows),
        "sampled_count": len(selected_rows),
        "approx_truncated_tokens": estimate_tokens(trunc_words),
        "bucket_summary": bucket_summary,
        "reviews": manifest_reviews,
    }
    return manifest, sampled_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 0 stratified sampling.")
    parser.add_argument("--csv", type=Path, default=ROOT / "inputs/raw/groww_playstore_reviews.csv")
    parser.add_argument("--manifest-out", type=Path, default=ROOT / "data/working/sample_manifest.json")
    parser.add_argument("--sample-out", type=Path, default=ROOT / "data/working/sampled_reviews.json")
    parser.add_argument("--seed", type=int, default=int(os.environ.get("SAMPLER_SEED", "42")))
    parser.add_argument(
        "--max-reviews",
        type=int,
        default=int(os.environ.get("SAMPLE_MAX_REVIEWS", "1000")),
    )
    parser.add_argument(
        "--text-max-chars",
        type=int,
        default=int(os.environ.get("STAGE_A_TEXT_MAX_CHARS", "320")),
    )
    parser.add_argument("--cap-negative", type=int, default=35)
    parser.add_argument("--cap-neutral", type=int, default=12)
    parser.add_argument("--cap-positive", type=int, default=8)
    args = parser.parse_args()

    if args.max_reviews < 1 or args.max_reviews > 1000:
        print("ERROR: --max-reviews must be between 1 and 1000", file=sys.stderr)
        return 1

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 1

    rows = load_reviews_csv(args.csv)
    tier_caps = {
        "negative": args.cap_negative,
        "neutral": args.cap_neutral,
        "positive": args.cap_positive,
    }

    manifest, payload = run_sampling(
        rows,
        seed=args.seed,
        global_max=args.max_reviews,
        text_max_chars=args.text_max_chars,
        tier_caps=tier_caps,
    )
    manifest["source_csv"] = str(args.csv.relative_to(ROOT)) if args.csv.is_relative_to(ROOT) else str(args.csv)

    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.sample_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"Wrote {args.manifest_out} and {args.sample_out} "
        f"({manifest['sampled_count']} / {manifest['corpus_row_count']} reviews, "
        f"~{manifest['approx_truncated_tokens']} truncated tokens)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
