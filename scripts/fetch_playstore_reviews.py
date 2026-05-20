#!/usr/bin/env python3
"""
Fetch and normalize public Google Play Store reviews using google-play-scraper.

Reads only publicly visible reviews (no login, no Play Console access).
Author names are NOT written to output (PII minimization).

Normalization rules applied after fetch:
  1. Keep only reviews with more than 6 words.
  2. Remove reviews that contain emoji characters.
  3. Remove reviews that contain non-English script (Devanagari, Bengali, etc.).
  4. Deduplicate by review_id.
  5. Filter to a rolling date window (--since-weeks).

Output CSV columns: rating,title,text,date,source_store,review_id

Usage:
  python3 scripts/fetch_playstore_reviews.py \\
    --package com.nextbillion.groww \\
    --count 15000 --since-weeks 12 \\
    --out inputs/raw/groww_playstore_reviews.csv
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from google_play_scraper import Sort, reviews

MIN_WORD_COUNT = 7  # keep reviews with more than 6 words (i.e. >= 7)

EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U0001FA70-\U0001FAFF"  # symbols extended-A
    "\U00002702-\U000027B0"  # dingbats
    "\U00002600-\U000026FF"  # misc symbols
    "\U00002B50-\U00002B55"  # stars
    "\U0000FE00-\U0000FE0F"  # variation selectors
    "\U0000200D"             # zero width joiner
    "\U00002764"             # heart
    "\U0000203C\U00002049"   # exclamation marks
    "\U0000231A-\U0000231B"
    "\U000023CF"
    "\U000023E9-\U000023F3"
    "\U000023F8-\U000023FA"
    "\U000025AA-\U000025FE"
    "\U00002934-\U00002935"
    "\U00002B05-\U00002B07"
    "\U00002B1B-\U00002B1C"
    "\U0000270A-\U0000270D"
    "\U00003030\U0000303D"
    "\U00003297\U00003299"
    "]"
)

NON_ENGLISH_SCRIPT_RE = re.compile(
    "["
    "\u0900-\u097F"  # Devanagari (Hindi, Marathi, etc.)
    "\u0980-\u09FF"  # Bengali
    "\u0A00-\u0A7F"  # Gurmukhi (Punjabi)
    "\u0A80-\u0AFF"  # Gujarati
    "\u0B00-\u0B7F"  # Odia
    "\u0B80-\u0BFF"  # Tamil
    "\u0C00-\u0C7F"  # Telugu
    "\u0C80-\u0CFF"  # Kannada
    "\u0D00-\u0D7F"  # Malayalam
    "\u0600-\u06FF"  # Arabic
    "\u4E00-\u9FFF"  # CJK
    "\uAC00-\uD7AF"  # Korean
    "\u0E00-\u0E7F"  # Thai
    "]"
)


def fetch_reviews(
    package: str,
    count: int,
    lang: str = "en",
    country: str = "in",
) -> List[Dict[str, Any]]:
    """Pull up to `count` reviews sorted by newest first."""
    all_reviews: List[Dict[str, Any]] = []
    continuation_token = None
    batch_size = min(count, 200)

    while len(all_reviews) < count:
        result, continuation_token = reviews(
            package,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=continuation_token,
        )
        if not result:
            break
        all_reviews.extend(result)
        if continuation_token is None:
            break

    return all_reviews[:count]


def normalize(raw: Dict[str, Any]) -> Dict[str, str]:
    dt_val = raw.get("at")
    date_str = ""
    if isinstance(dt_val, datetime):
        date_str = dt_val.date().isoformat()
    elif isinstance(dt_val, str) and len(dt_val) >= 10:
        date_str = dt_val[:10]

    return {
        "rating": str(raw.get("score", "")),
        "title": "",
        "text": (raw.get("content") or "").replace("\n", " ").strip(),
        "date": date_str,
        "source_store": "play_store",
        "review_id": raw.get("reviewId", ""),
    }


def passes_quality_filters(text: str) -> bool:
    """Return True if the review text passes all normalization rules."""
    if len(text.split()) < MIN_WORD_COUNT:
        return False
    if EMOJI_RE.search(text):
        return False
    if NON_ENGLISH_SCRIPT_RE.search(text):
        return False
    return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--package", required=True, help="Play Store package name (e.g. com.nextbillion.groww)"
    )
    p.add_argument("--out", required=True, help="Output CSV path")
    p.add_argument("--count", type=int, default=15000, help="Max reviews to fetch (before filtering)")
    p.add_argument(
        "--since-weeks",
        type=int,
        default=12,
        help="Keep only reviews from the last N weeks (0 disables filter)",
    )
    p.add_argument("--lang", default="en", help="Review language (default en)")
    p.add_argument("--country", default="in", help="Country code (default in)")
    args = p.parse_args()

    print(f"fetch: pulling up to {args.count} reviews for {args.package} ...")
    raw_reviews = fetch_reviews(args.package, args.count, lang=args.lang, country=args.country)
    print(f"fetch: received {len(raw_reviews)} raw reviews")

    cutoff: Optional[date] = None
    if args.since_weeks and args.since_weeks > 0:
        cutoff = date.today() - timedelta(weeks=args.since_weeks)

    rows: List[Dict[str, str]] = []
    seen: set = set()
    skipped_date = 0
    skipped_quality = 0
    skipped_dup = 0

    for r in raw_reviews:
        n = normalize(r)
        rid = n["review_id"]
        if rid in seen:
            skipped_dup += 1
            continue
        seen.add(rid)
        if cutoff and n["date"]:
            try:
                if date.fromisoformat(n["date"]) < cutoff:
                    skipped_date += 1
                    continue
            except ValueError:
                pass
        if not passes_quality_filters(n["text"]):
            skipped_quality += 1
            continue
        rows.append(n)

    print(f"filter: skipped {skipped_dup} duplicates, "
          f"{skipped_date} outside date window, "
          f"{skipped_quality} failed quality (<=6 words / emoji / non-English)")

    if not rows:
        print("fetch: no reviews after filtering.", file=sys.stderr)
        return 2

    fieldnames = ["rating", "title", "text", "date", "source_store", "review_id"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    dates = [r["date"] for r in rows if r.get("date")]
    span = f"{min(dates)} .. {max(dates)}" if dates else "(no dates)"
    print(f"fetch: wrote {len(rows)} normalized rows to {args.out}")
    print(f"fetch: date span: {span}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
