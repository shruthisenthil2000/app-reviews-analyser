#!/usr/bin/env python3
"""
Compute deterministic corpus statistics for Stage A/B prompts.

Reads:  inputs/raw/groww_playstore_reviews.csv (default)
Writes: data/working/corpus_stats.json

Usage:
  python3 scripts/corpus_stats.py
  python3 scripts/corpus_stats.py --csv inputs/raw/groww_playstore_reviews.csv --out data/working/corpus_stats.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import (  # noqa: E402
    TOPIC_KEYWORDS,
    ReviewRow,
    estimate_tokens,
    load_reviews_csv,
    top_bigrams,
    topic_hits,
    utc_now_iso,
)


def build_stats(rows: List[ReviewRow]) -> Dict[str, Any]:
    rating_counts: Counter[int] = Counter()
    rating_words: Dict[int, List[int]] = defaultdict(list)
    weekly: Dict[str, Dict[str, int]] = defaultdict(lambda: {"reviews": 0, "words": 0})
    topic_counts: Counter[str] = Counter()
    topic_rating_sum: Dict[str, int] = defaultdict(int)
    topic_rating_n: Dict[str, int] = defaultdict(int)

    total_words = 0
    word_lengths: List[int] = []

    for row in rows:
        rating_counts[row.rating] += 1
        wc = row.word_count
        rating_words[row.rating].append(wc)
        total_words += wc
        word_lengths.append(wc)

        weekly[row.iso_week]["reviews"] += 1
        weekly[row.iso_week]["words"] += wc

        lower = row.text.lower()
        for topic in topic_hits(lower):
            topic_counts[topic] += 1
            topic_rating_sum[topic] += row.rating
            topic_rating_n[topic] += 1

    def avg(words_list: List[int]) -> float:
        return round(sum(words_list) / len(words_list), 2) if words_list else 0.0

    rating_distribution = []
    for star in sorted(rating_counts):
        rating_distribution.append(
            {
                "rating": star,
                "count": rating_counts[star],
                "share_pct": round(100 * rating_counts[star] / len(rows), 1),
                "avg_words": avg(rating_words[star]),
            }
        )

    weekly_trends = []
    for week in sorted(weekly):
        w = weekly[week]
        weekly_trends.append(
            {
                "iso_week": week,
                "reviews": w["reviews"],
                "words": w["words"],
                "approx_tokens": estimate_tokens(w["words"]),
            }
        )

    topics = []
    for topic in sorted(topic_counts, key=lambda t: (-topic_counts[t], t)):
        n = topic_rating_n[topic]
        topics.append(
            {
                "topic": topic,
                "review_count": topic_counts[topic],
                "share_pct": round(100 * topic_counts[topic] / len(rows), 1),
                "avg_rating": round(topic_rating_sum[topic] / n, 2) if n else None,
            }
        )

    sorted_lengths = sorted(word_lengths)
    mid = len(sorted_lengths) // 2

    return {
        "schema_version": "1.0",
        "product": "com.nextbillion.groww",
        "generated_at": utc_now_iso(),
        "corpus": {
            "row_count": len(rows),
            "total_words": total_words,
            "approx_tokens": estimate_tokens(total_words),
            "avg_words_per_review": round(total_words / len(rows), 2) if rows else 0,
            "median_words_per_review": sorted_lengths[mid] if sorted_lengths else 0,
            "max_words_in_review": max(word_lengths) if word_lengths else 0,
        },
        "rating_distribution": rating_distribution,
        "weekly_trends": weekly_trends,
        "topic_prevalence": topics,
        "topic_keywords": {k: v for k, v in TOPIC_KEYWORDS.items()},
        "top_bigrams": [{"bigram": b, "count": c} for b, c in top_bigrams((r.text for r in rows), 25)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute corpus statistics JSON.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=ROOT / "inputs/raw/groww_playstore_reviews.csv",
        help="Normalized reviews CSV",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data/working/corpus_stats.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 1

    rows = load_reviews_csv(args.csv)
    if not rows:
        print("ERROR: no rows in CSV", file=sys.stderr)
        return 1

    stats = build_stats(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {args.out} ({stats['corpus']['row_count']} reviews)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
