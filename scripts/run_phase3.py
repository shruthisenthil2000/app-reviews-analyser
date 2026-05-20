#!/usr/bin/env python3
"""
Phase 3 entry point: Stage 0 → Groq A/B → validation → artifacts (MCP-ready).

Prerequisites:
  - GROQ_API_KEY in .env
  - inputs/raw/groww_playstore_reviews.csv

Usage:
  python3 scripts/run_phase3.py --quota-safe          # recommended (280 reviews)
  python3 scripts/run_phase3.py --validate-only       # check existing outputs
  python3 scripts/run_phase3.py --skip-groq --validate-only  # finalize from disk

Phase 4 MCP (separate): use artifacts/mcp_delivery.json with Saksham MCP server.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import load_dotenv  # noqa: E402
from scripts.pipeline.finalize import finalize_phase3_run  # noqa: E402

WORKING = ROOT / "data/working"
MAX_CHUNKS_WITHOUT_FORCE = 12


def estimate_chunk_count() -> int:
    preflight = WORKING / "preflight_estimate.json"
    if preflight.is_file():
        return int(json.loads(preflight.read_text()).get("estimated_stage_a_chunks", 0))
    return 0


def main() -> int:
    load_dotenv()
    import os

    default_doc = os.environ.get("GOOGLE_DOC_ID", "").strip()
    default_email = os.environ.get("PULSE_TO_EMAIL", "").strip()

    parser = argparse.ArgumentParser(description="Phase 3: Groq pulse pipeline + validation.")
    parser.add_argument("--skip-prep", action="store_true")
    parser.add_argument(
        "--no-quota-safe",
        action="store_true",
        help="Sample up to 1000 reviews (may exceed Groq 100k TPD)",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stage-b-only", action="store_true")
    parser.add_argument("--skip-groq", action="store_true", help="Skip Groq calls; only validate/finalize")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--force", action="store_true", help="Run even if chunk estimate exceeds TPD guard")
    parser.add_argument("--week-label", default="")
    parser.add_argument(
        "--to-email",
        default=default_email,
        help="Recipient for mcp_delivery.json (default: PULSE_TO_EMAIL from .env)",
    )
    parser.add_argument(
        "--doc-id",
        default=default_doc,
        help="Google Doc ID for mcp_delivery.json (default: GOOGLE_DOC_ID from .env)",
    )
    args = parser.parse_args()

    quota_safe = not args.no_quota_safe

    if not args.validate_only and not args.skip_groq:
        cmd = [sys.executable, str(ROOT / "scripts/run_weekly_pulse.py")]
        if args.skip_prep:
            cmd.append("--skip-prep")
        if quota_safe:
            cmd.append("--quota-safe")
        if args.resume:
            cmd.append("--resume")
        if args.stage_b_only:
            cmd.append("--stage-b-only")
        if args.week_label:
            cmd.extend(["--week-label", args.week_label])

        if not args.stage_b_only:
            if not args.skip_prep:
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts/corpus_stats.py")],
                    check=True,
                    cwd=ROOT,
                )
            if quota_safe and not args.skip_prep:
                pass  # quota-safe handled inside run_weekly_pulse
            elif not args.skip_prep:
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts/stage0_sample.py")],
                    check=True,
                    cwd=ROOT,
                )
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts/preflight_tokens.py")],
                    check=True,
                    cwd=ROOT,
                )
            n_chunks = estimate_chunk_count()
            if n_chunks > MAX_CHUNKS_WITHOUT_FORCE and not args.force:
                print(
                    f"ERROR: estimated {n_chunks} Stage A chunks may exceed 100k TPD. "
                    f"Use --quota-safe (default) or --force.",
                    file=sys.stderr,
                )
                return 1

        print("== Phase 3: Groq pipeline ==")
        proc = subprocess.run(cmd, cwd=ROOT)
        if proc.returncode != 0:
            return proc.returncode

    print("== Phase 3: validation & finalize ==")
    try:
        manifest = finalize_phase3_run(
            week_label=args.week_label,
            to_email=args.to_email,
            doc_id=args.doc_id,
        )
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if not manifest["validation"]["valid"]:
        print("VALIDATION FAILED")
        print(json.dumps(manifest["validation"], indent=2))
        return 1

    print("VALIDATION OK")
    print(f"  Pulse words: {manifest['validation']['pulse_word_count']}")
    print(f"  Themes: {manifest['validation']['theme_count']}")
    print(f"  Run manifest: runs/phase-03/run_manifest.json")
    print(f"  MCP handoff: artifacts/mcp_delivery.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
