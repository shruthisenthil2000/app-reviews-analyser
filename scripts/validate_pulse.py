#!/usr/bin/env python3
"""
Validate Stage A/B outputs on disk (Phase 3 gate).

Usage:
  python3 scripts/validate_pulse.py
  python3 scripts/validate_pulse.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import load_reviews_csv  # noqa: E402
from scripts.pipeline.validate_output import validate_pulse_package  # noqa: E402

WORKING = ROOT / "data/working"
CSV_PATH = ROOT / "inputs/raw/groww_playstore_reviews.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pulse JSON artifacts.")
    parser.add_argument("--json", action="store_true", help="Print JSON report only")
    args = parser.parse_args()

    stage_a_path = WORKING / "stage_a_merged.json"
    stage_b_path = WORKING / "stage_b_output.json"
    for p in (stage_a_path, stage_b_path):
        if not p.is_file():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 1

    stage_a = json.loads(stage_a_path.read_text(encoding="utf-8"))
    stage_b = json.loads(stage_b_path.read_text(encoding="utf-8"))
    rows = load_reviews_csv(CSV_PATH)
    corpus_ids = {r.review_id for r in rows}
    id_to_text = {r.review_id: r.text for r in rows}
    sampled_ids = corpus_ids
    manifest = WORKING / "sample_manifest.json"
    if manifest.is_file():
        sampled_ids = {
            r["review_id"]
            for r in json.loads(manifest.read_text(encoding="utf-8")).get("reviews", [])
        }

    report = validate_pulse_package(stage_a, stage_b, corpus_ids, sampled_ids, id_to_text)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Valid: {report['valid']}")
        print(f"Themes: {report['theme_count']} | Pulse words: {report['pulse_word_count']}")
        if report["stage_a_errors"]:
            print("Stage A errors:", report["stage_a_errors"])
        if report["stage_b_errors"]:
            print("Stage B errors:", report["stage_b_errors"])
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
