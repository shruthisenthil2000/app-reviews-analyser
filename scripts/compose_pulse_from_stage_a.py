#!/usr/bin/env python3
"""
Build a readable pulse artifact from stage_a_merged.json when Groq Stage B is blocked (TPD).

Usage:
  python3 scripts/compose_pulse_from_stage_a.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import load_dotenv, load_reviews_csv  # noqa: E402

WORKING = ROOT / "data/working"
ARTIFACTS = ROOT / "artifacts"
CSV_PATH = ROOT / "inputs/raw/groww_playstore_reviews.csv"


def main() -> int:
    load_dotenv()
    stage_a_path = WORKING / "stage_a_merged.json"
    if not stage_a_path.is_file():
        print("ERROR: run Stage A first (stage_a_merged.json missing)", file=sys.stderr)
        return 1

    stage_a = json.loads(stage_a_path.read_text(encoding="utf-8"))
    themes = sorted(stage_a.get("themes", []), key=lambda t: t.get("rank", 99))[:3]
    rows = load_reviews_csv(CSV_PATH)
    id_to_text = {r.review_id: r.text for r in rows}

    lines = [f"Weekly App Review Pulse — Groww — {date.today().strftime('%G-W%V')}", ""]
    lines.append(
        "This week, Play Store reviews highlight recurring friction across support, fees, and reliability."
    )
    lines.append("")
    for t in themes:
        lines.append(f"• {t['label']}: {t['summary']}")
    lines.append("")
    lines.append("User voices (from cited reviews)")
    quotes_out = []
    for i, t in enumerate(themes, 1):
        rid = (t.get("evidence_review_ids") or [None])[0]
        snippet = id_to_text.get(rid, "")[:200] if rid else t["summary"][:200]
        if len(snippet) > 197:
            snippet = snippet[:197] + "…"
        lines.append(f'{i}. "{snippet}"')
        quotes_out.append({"text": snippet, "review_ids": [rid] if rid else []})
    lines.append("")
    lines.append("Suggested actions")
    actions = [
        ("Improve support SLAs and escalation paths", themes[0]["label"] if themes else "support"),
        ("Review brokerage and fee transparency in-app", themes[0]["label"] if themes else "fees"),
        ("Stabilize withdrawals and order execution", themes[-1]["label"] if themes else "reliability"),
    ]
    for i, (title, topic) in enumerate(actions, 1):
        lines.append(f"{i}. {title} — Address feedback on {topic.lower()}.")

    week = date.today().strftime("%G-W%V")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / f"pulse_{week}_draft.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    stage_b = {
        "pulse_body": " ".join(
            [
                lines[2],
                " ".join(lines[4:4 + len(themes)]),
            ]
        )[:2000],
        "quotes": quotes_out[:3],
        "actions": [
            {"title": a[0], "rationale": f"Grounded in theme: {a[1]}."} for a in actions
        ],
    }
    (WORKING / "stage_b_output.json").write_text(
        json.dumps(stage_b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {ARTIFACTS / f'pulse_{week}_draft.txt'} (local draft; re-run Stage B via Groq when TPD resets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
