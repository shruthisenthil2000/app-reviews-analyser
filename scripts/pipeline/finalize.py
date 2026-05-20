"""Phase 3 finalize: validation report, golden run copy, MCP handoff payload."""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path
from typing import Any, Dict, Set

from scripts.pipeline.common import ROOT, load_reviews_csv, utc_now_iso
from scripts.pipeline.pulse_render import build_mcp_delivery, render_pulse_plain
from scripts.pipeline.validate_output import validate_pulse_package

WORKING = ROOT / "data/working"
ARTIFACTS = ROOT / "artifacts"
RUNS_P3 = ROOT / "runs/phase-03"
CSV_PATH = ROOT / "inputs/raw/groww_playstore_reviews.csv"


def finalize_phase3_run(
    *,
    week_label: str = "",
    to_email: str = "",
    doc_id: str = "",
) -> Dict[str, Any]:
    week = week_label or date.today().strftime("%G-W%V")
    stage_a_path = WORKING / "stage_a_merged.json"
    stage_b_path = WORKING / "stage_b_output.json"
    if not stage_a_path.is_file() or not stage_b_path.is_file():
        raise FileNotFoundError("Missing stage_a_merged.json or stage_b_output.json")

    stage_a = json.loads(stage_a_path.read_text(encoding="utf-8"))
    stage_b = json.loads(stage_b_path.read_text(encoding="utf-8"))
    rows = load_reviews_csv(CSV_PATH)
    corpus_ids = {r.review_id for r in rows}
    id_to_text = {r.review_id: r.text for r in rows}

    sampled_ids: Set[str] = corpus_ids
    manifest = WORKING / "sample_manifest.json"
    if manifest.is_file():
        sampled_ids = {r["review_id"] for r in json.loads(manifest.read_text(encoding="utf-8")).get("reviews", [])}

    report = validate_pulse_package(stage_a, stage_b, corpus_ids, sampled_ids, id_to_text)

    plain = render_pulse_plain(stage_b, week)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    pulse_txt = ARTIFACTS / f"pulse_{week}.txt"
    pulse_txt.write_text(plain, encoding="utf-8")

    mcp_payload = build_mcp_delivery(stage_b, week_label=week, to_email=to_email, doc_id=doc_id)
    (ARTIFACTS / "mcp_delivery.json").write_text(
        json.dumps(mcp_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    RUNS_P3.mkdir(parents=True, exist_ok=True)
    for name in ("stage_a_merged.json", "stage_b_output.json", "sample_manifest.json", "preflight_estimate.json"):
        src = WORKING / name
        if src.is_file():
            shutil.copy2(src, RUNS_P3 / name)
    shutil.copy2(pulse_txt, RUNS_P3 / pulse_txt.name)

    manifest_out = {
        "schema_version": "1.0",
        "completed_at": utc_now_iso(),
        "week_label": week,
        "validation": report,
        "artifacts": {
            "pulse_text": str(pulse_txt.relative_to(ROOT)),
            "mcp_delivery": "artifacts/mcp_delivery.json",
        },
    }
    (RUNS_P3 / "run_manifest.json").write_text(
        json.dumps(manifest_out, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_out
