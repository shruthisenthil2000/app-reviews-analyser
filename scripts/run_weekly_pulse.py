#!/usr/bin/env python3
"""
Run Phase 2 prep + Groq Stage A (themes) + Stage B (weekly pulse).

Prerequisites: GROQ_API_KEY in .env

Usage:
  python3 scripts/run_weekly_pulse.py
  python3 scripts/run_weekly_pulse.py --skip-prep   # use existing data/working/*.json
  GROQ_PACE_SECONDS=5 python3 scripts/run_weekly_pulse.py  # faster pacing (dev only)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Set

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import (  # noqa: E402
    ROOT as PROJECT_ROOT,
    load_dotenv,
    load_reviews_csv,
)
from scripts.pipeline.groq_client import chat_json, pace, require_api_key  # noqa: E402
from scripts.pipeline.merge_themes import merge_stage_a_outputs  # noqa: E402
from scripts.pipeline.pulse_render import render_pulse_plain  # noqa: E402
from scripts.pipeline.validate_output import validate_stage_a, validate_stage_b  # noqa: E402

PROMPTS = PROJECT_ROOT / "docs/phases/phase-02/prompts"
WORKING = PROJECT_ROOT / "data/working"
ARTIFACTS = PROJECT_ROOT / "artifacts"
CSV_PATH = PROJECT_ROOT / "inputs/raw/groww_playstore_reviews.csv"
# Serialized user JSON budget (~9k tokens target per architecture §6.1)
# Keep each Stage A request under ~9k tokens (12k TPM limit on Groq free tier)
CHUNK_PAYLOAD_MAX_CHARS = 14_000


def load_prompt_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "---" in text:
        return text.split("---", 2)[-1].strip()
    return text.strip()


def compact_stats(stats: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "corpus": stats.get("corpus"),
        "rating_distribution": stats.get("rating_distribution"),
        "weekly_trends": (stats.get("weekly_trends") or [])[-8:],
        "topic_prevalence": (stats.get("topic_prevalence") or [])[:8],
        "top_bigrams": (stats.get("top_bigrams") or [])[:10],
    }


def chunk_sampled_reviews(
    reviews: List[Dict[str, Any]],
    stats: Dict[str, Any],
    max_payload_chars: int = CHUNK_PAYLOAD_MAX_CHARS,
) -> List[List[Dict[str, Any]]]:
    stats_len = len(json.dumps(stats, ensure_ascii=False))
    chunks: List[List[Dict[str, Any]]] = []
    current: List[Dict[str, Any]] = []
    current_len = stats_len

    for row in reviews:
        row_len = len(json.dumps(row, ensure_ascii=False))
        if current and current_len + row_len > max_payload_chars:
            chunks.append(current)
            current = []
            current_len = stats_len
        current.append(row)
        current_len += row_len

    if current:
        chunks.append(current)
    return chunks


def run_prep() -> None:
    for script in ("corpus_stats.py", "stage0_sample.py", "preflight_tokens.py"):
        subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / script)], check=True, cwd=PROJECT_ROOT)


def slim_reviews_for_prompt(chunk: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "review_id": r["review_id"],
            "rating": r["rating"],
            "text": r.get("text_truncated") or r.get("text", ""),
        }
        for r in chunk
    ]


def call_stage_a_chunk(
    *,
    api_key: str,
    system: str,
    stats: Dict[str, Any],
    chunk: List[Dict[str, Any]],
    allowed_ids: List[str],
    chunk_index: int,
    total_chunks: int,
    repair: bool = False,
) -> Dict[str, Any]:
    user_payload = {
        "chunk": f"{chunk_index + 1} of {total_chunks}",
        "corpus_statistics": stats,
        "sampled_reviews": slim_reviews_for_prompt(chunk),
        "allowed_review_ids": allowed_ids,
    }
    user = json.dumps(user_payload, ensure_ascii=False)
    if repair:
        user += (
            "\n\nYour previous response was invalid. Return JSON only with themes[]."
            " Every evidence_review_id MUST be in allowed_review_ids."
        )
    return chat_json(api_key=api_key, system=system, user=user)


def call_stage_b(
    *,
    api_key: str,
    system: str,
    stage_a: Dict[str, Any],
    evidence_reviews: List[Dict[str, str]],
    stats: Dict[str, Any],
    repair: bool = False,
) -> Dict[str, Any]:
    user_payload = {
        "stage_a_themes": stage_a,
        "evidence_reviews": evidence_reviews,
        "corpus_statistics_summary": {
            "row_count": stats.get("corpus", {}).get("row_count"),
            "topic_prevalence": (stats.get("topic_prevalence") or [])[:5],
        },
    }
    user = json.dumps(user_payload, ensure_ascii=False)
    if repair:
        user += (
            "\n\nPrevious response invalid. Return JSON with pulse_body (<=250 words),"
            " exactly 3 quotes and 3 actions. All review_ids must exist in evidence_reviews."
        )
    return chat_json(api_key=api_key, system=system, user=user, max_tokens=3000)


def collect_evidence_texts(
    stage_a: Dict[str, Any],
    id_to_text: Dict[str, str],
    max_per_theme: int = 5,
    max_total: int = 20,
) -> List[Dict[str, str]]:
    seen: Set[str] = set()
    out: List[Dict[str, str]] = []
    for theme in stage_a.get("themes", []):
        per_theme = 0
        for rid in theme.get("evidence_review_ids", []):
            if per_theme >= max_per_theme or len(out) >= max_total:
                break
            if rid in seen or rid not in id_to_text:
                continue
            seen.add(rid)
            per_theme += 1
            text = id_to_text[rid]
            if len(text) > 600:
                text = text[:599] + "\u2026"
            out.append({"review_id": rid, "text": text})
    return out


def load_and_merge_stage_a(all_sampled_ids: Set[str]) -> Dict[str, Any]:
    paths = sorted(WORKING.glob("stage_a_chunk_*.json"), key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
    if not paths:
        raise RuntimeError("No stage_a_chunk_*.json files found")
    chunk_outputs = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    stage_a = merge_stage_a_outputs(chunk_outputs)
    for theme in stage_a.get("themes", []):
        theme["evidence_review_ids"] = [
            rid for rid in theme.get("evidence_review_ids", []) if rid in all_sampled_ids
        ]
    return stage_a


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run weekly pulse: Stage 0 prep + Groq A/B.")
    parser.add_argument("--skip-prep", action="store_true", help="Use existing data/working JSON")
    parser.add_argument("--resume", action="store_true", help="Skip Stage A chunks that already have output files")
    parser.add_argument(
        "--stage-b-only",
        action="store_true",
        help="Merge existing stage_a_chunk_*.json and run Stage B only",
    )
    parser.add_argument("--week-label", default="", help="Label for artifact (default: today ISO week)")
    parser.add_argument(
        "--quota-safe",
        action="store_true",
        help="Re-sample at 280 reviews (fits ~100k TPD) before Groq stages",
    )
    args = parser.parse_args()

    if args.quota_safe:
        subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "scripts/stage0_sample.py"),
                "--max-reviews",
                "280",
            ],
            check=True,
            cwd=PROJECT_ROOT,
        )
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/preflight_tokens.py")],
            check=True,
            cwd=PROJECT_ROOT,
        )
        sampled = json.loads((WORKING / "sampled_reviews.json").read_text(encoding="utf-8"))
        print(f"== Quota-safe sample: {len(sampled)} reviews ==")

    if not args.skip_prep and not args.stage_b_only:
        print("== Phase 2 prep: corpus stats, Stage 0 sample, preflight ==")
        run_prep()

    preflight_path = WORKING / "preflight_estimate.json"
    if preflight_path.is_file():
        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        if not preflight.get("within_tpd", True):
            print("ERROR: preflight_estimate.json reports within_tpd=false", file=sys.stderr)
            return 1

    stats = json.loads((WORKING / "corpus_stats.json").read_text(encoding="utf-8"))
    sampled = json.loads((WORKING / "sampled_reviews.json").read_text(encoding="utf-8"))
    all_sampled_ids = {r["review_id"] for r in sampled}

    api_key = require_api_key()
    system_a = load_prompt_md(PROMPTS / "stage_a_system.md")
    system_b = load_prompt_md(PROMPTS / "stage_b_system.md")
    stats_compact = compact_stats(stats)

    if args.stage_b_only:
        stage_a = load_and_merge_stage_a(all_sampled_ids)
        (WORKING / "stage_a_merged.json").write_text(
            json.dumps(stage_a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"== Stage A merged from disk: {len(stage_a.get('themes', []))} themes ==")
        for t in stage_a.get("themes", []):
            print(f"  #{t['rank']} {t['label']}")
        stage_a_for_b = {
            "themes": [
                {
                    "rank": t["rank"],
                    "label": t["label"],
                    "summary": t["summary"],
                    "evidence_review_ids": (t.get("evidence_review_ids") or [])[:5],
                }
                for t in stage_a.get("themes", [])[:3]
            ]
        }
        rows = load_reviews_csv(CSV_PATH)
        id_to_text = {r.review_id: r.text for r in rows}
        evidence = collect_evidence_texts(stage_a_for_b, id_to_text, max_per_theme=2, max_total=8)
        print(f"== Stage B: pulse draft ({len(evidence)} evidence reviews) ==")
        stage_b = call_stage_b(
            api_key=api_key,
            system=load_prompt_md(PROMPTS / "stage_b_system.md"),
            stage_a=stage_a_for_b,
            evidence_reviews=evidence,
            stats=stats,
        )
        errors = validate_stage_b(stage_b, set(id_to_text), id_to_text=id_to_text)
        if errors:
            print(f"ERROR Stage B: {errors}", file=sys.stderr)
            return 1
        (WORKING / "stage_b_output.json").write_text(
            json.dumps(stage_b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        week_label = args.week_label or date.today().strftime("%G-W%V")
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        pulse_path = ARTIFACTS / f"pulse_{week_label}.txt"
        pulse_path.write_text(render_pulse_plain(stage_b, week_label), encoding="utf-8")
        print(f"\n== Done ==\n  Pulse: {pulse_path}")
        return 0

    chunks = chunk_sampled_reviews(sampled, stats_compact)
    print(f"== Stage A: {len(chunks)} chunk(s), {len(sampled)} sampled reviews ==")

    chunk_outputs: List[Dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        out_path = WORKING / f"stage_a_chunk_{i}.json"
        if args.resume and out_path.is_file():
            print(f"  Skipping chunk {i + 1}/{len(chunks)} (already on disk)")
            chunk_outputs.append(json.loads(out_path.read_text(encoding="utf-8")))
            continue

        chunk_ids = {r["review_id"] for r in chunk}
        allowed_list = sorted(chunk_ids)
        print(f"  Groq Stage A chunk {i + 1}/{len(chunks)} ({len(chunk)} reviews)...")
        result = call_stage_a_chunk(
            api_key=api_key,
            system=system_a,
            stats=stats_compact if i == 0 else {"note": "see chunk 1 for full corpus statistics"},
            chunk=chunk,
            allowed_ids=allowed_list,
            chunk_index=i,
            total_chunks=len(chunks),
        )
        errors = validate_stage_a(result, chunk_ids)
        if errors:
            print(f"  Validation failed, one retry: {errors[:3]}")
            pace()
            result = call_stage_a_chunk(
                api_key=api_key,
                system=system_a,
                stats=stats_compact if i == 0 else {"note": "see chunk 1 for full corpus statistics"},
                chunk=chunk,
                allowed_ids=allowed_list,
                chunk_index=i,
                total_chunks=len(chunks),
                repair=True,
            )
            errors = validate_stage_a(result, chunk_ids)
            if errors:
                print(f"ERROR Stage A chunk {i}: {errors}", file=sys.stderr)
                return 1

        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        chunk_outputs.append(result)
        if i < len(chunks) - 1:
            pace()

    stage_a = merge_stage_a_outputs(chunk_outputs)
    for theme in stage_a.get("themes", []):
        theme["evidence_review_ids"] = [
            rid for rid in theme.get("evidence_review_ids", []) if rid in all_sampled_ids
        ]
    (WORKING / "stage_a_merged.json").write_text(
        json.dumps(stage_a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"== Stage A merged: {len(stage_a.get('themes', []))} themes ==")
    for t in stage_a.get("themes", []):
        print(f"  #{t['rank']} {t['label']} ({len(t.get('evidence_review_ids', []))} ids)")

    pace()

    rows = load_reviews_csv(CSV_PATH)
    id_to_text = {r.review_id: r.text for r in rows}
    corpus_ids = set(id_to_text)
    evidence = collect_evidence_texts(stage_a, id_to_text)

    print(f"== Stage B: pulse draft ({len(evidence)} evidence reviews) ==")
    stage_b = call_stage_b(
        api_key=api_key,
        system=system_b,
        stage_a=stage_a,
        evidence_reviews=evidence,
        stats=stats,
    )
    errors = validate_stage_b(stage_b, corpus_ids, id_to_text=id_to_text)
    if errors:
        print(f"  Validation failed, one retry: {errors[:3]}")
        pace()
        stage_b = call_stage_b(
            api_key=api_key,
            system=system_b,
            stage_a=stage_a,
            evidence_reviews=evidence,
            stats=stats,
            repair=True,
        )
        errors = validate_stage_b(stage_b, corpus_ids, id_to_text=id_to_text)
        if errors:
            print(f"ERROR Stage B: {errors}", file=sys.stderr)
            return 1

    (WORKING / "stage_b_output.json").write_text(
        json.dumps(stage_b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    week_label = args.week_label or date.today().strftime("%G-W%V")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    pulse_path = ARTIFACTS / f"pulse_{week_label}.txt"
    pulse_path.write_text(render_pulse_plain(stage_b, week_label), encoding="utf-8")

    print(f"\n== Done ==")
    print(f"  Themes: {WORKING / 'stage_a_merged.json'}")
    print(f"  Pulse:  {WORKING / 'stage_b_output.json'}")
    print(f"  Plain:  {pulse_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
