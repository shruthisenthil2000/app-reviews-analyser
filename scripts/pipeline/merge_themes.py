"""Deterministic merge of per-chunk Stage A theme JSON."""
from __future__ import annotations

import re
from typing import Any, Dict, List


def normalize_label_key(label: str) -> str:
    """Collapse near-duplicate labels (e.g. 'brokerage fees' vs 'brokerage charges')."""
    s = label.lower().strip()
    s = re.sub(r"\b(fees?|charges?|issues?|problems?|glitches?)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def merge_stage_a_outputs(chunk_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged: Dict[str, Dict[str, Any]] = {}

    for output in chunk_outputs:
        for theme in output.get("themes", []):
            label_key = normalize_label_key(theme.get("label", ""))
            if not label_key:
                continue
            ids = theme.get("evidence_review_ids") or []
            if label_key not in merged:
                merged[label_key] = {
                    "label": theme.get("label", "").strip(),
                    "summary": theme.get("summary", "").strip(),
                    "evidence_review_ids": set(ids),
                    "best_rank": int(theme.get("rank", 99)),
                }
            else:
                entry = merged[label_key]
                entry["evidence_review_ids"].update(ids)
                entry["best_rank"] = min(entry["best_rank"], int(theme.get("rank", 99)))
                if len(theme.get("summary", "")) > len(entry["summary"]):
                    entry["summary"] = theme.get("summary", "").strip()
                    entry["label"] = theme.get("label", "").strip()

    themes_list = sorted(
        merged.values(),
        key=lambda t: (t["best_rank"], -len(t["evidence_review_ids"])),
    )[:5]

    themes: List[Dict[str, Any]] = []
    for i, t in enumerate(themes_list, start=1):
        themes.append(
            {
                "rank": i,
                "label": t["label"],
                "summary": t["summary"],
                "evidence_review_ids": sorted(t["evidence_review_ids"])[:25],
            }
        )

    return {"themes": themes}
