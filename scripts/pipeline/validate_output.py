"""Deterministic validation for Stage A/B outputs (Phase 3)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PII_PATTERNS = [
    re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    re.compile(r"@\w{3,}"),
    re.compile(r"\b\d{10,}\b"),
]

WORD_RE = re.compile(r"[a-z0-9']+")


def _scan_pii(text: str) -> List[str]:
    hits = []
    for pat in PII_PATTERNS:
        if pat.search(text):
            hits.append(pat.pattern)
    return hits


def _word_count(text: str) -> int:
    return len(text.split())


def _token_set(text: str) -> Set[str]:
    return set(WORD_RE.findall(text.lower()))


def quote_overlap_score(quote: str, source_text: str) -> float:
    q, s = _token_set(quote), _token_set(source_text)
    if not q or not s:
        return 0.0
    return len(q & s) / len(q)


def validate_stage_a(data: Dict[str, Any], allowed_ids: Set[str]) -> List[str]:
    errors: List[str] = []
    themes = data.get("themes")
    if not isinstance(themes, list) or not themes:
        errors.append("themes must be a non-empty list")
        return errors
    if len(themes) > 5:
        errors.append("at most 5 themes allowed")
    ranks = []
    for theme in themes:
        for field in ("rank", "label", "summary", "evidence_review_ids"):
            if field not in theme:
                errors.append(f"missing field: {field}")
        ranks.append(theme.get("rank"))
        ids = theme.get("evidence_review_ids") or []
        if not ids:
            errors.append(f"theme '{theme.get('label')}' has no evidence_review_ids")
        for rid in ids:
            if rid not in allowed_ids:
                errors.append(f"unknown evidence review_id: {rid}")
    if ranks and len(ranks) != len(set(ranks)):
        errors.append("duplicate theme ranks")
    return errors


def validate_stage_b(
    data: Dict[str, Any],
    corpus_ids: Set[str],
    id_to_text: Optional[Dict[str, str]] = None,
    max_words: int = 250,
    min_quote_overlap: float = 0.12,
) -> List[str]:
    errors: List[str] = []
    body = data.get("pulse_body", "")
    if not isinstance(body, str) or not body.strip():
        errors.append("pulse_body missing")
    else:
        wc = _word_count(body)
        if wc > max_words:
            errors.append(f"pulse_body has {wc} words (max {max_words})")
        if wc < 40:
            errors.append(f"pulse_body too short ({wc} words)")
        for pat in _scan_pii(body):
            errors.append(f"PII pattern in pulse_body: {pat}")

    quotes = data.get("quotes")
    if not isinstance(quotes, list) or len(quotes) != 3:
        errors.append("quotes must contain exactly 3 items")
    else:
        for i, q in enumerate(quotes):
            if not q.get("text"):
                errors.append(f"quote {i} missing text")
            ids = q.get("review_ids") or []
            if not ids:
                errors.append(f"quote {i} missing review_ids")
            for rid in ids:
                if rid not in corpus_ids:
                    errors.append(f"quote {i} unknown review_id: {rid}")
            for pat in _scan_pii(q.get("text", "")):
                errors.append(f"PII in quote {i}")
            if id_to_text and ids:
                sources = " ".join(id_to_text.get(rid, "") for rid in ids)
                if quote_overlap_score(q.get("text", ""), sources) < min_quote_overlap:
                    errors.append(f"quote {i} weak provenance overlap with cited review(s)")

    actions = data.get("actions")
    if not isinstance(actions, list) or len(actions) != 3:
        errors.append("actions must contain exactly 3 items")
    else:
        for i, a in enumerate(actions):
            if not a.get("title") or not a.get("rationale"):
                errors.append(f"action {i} missing title or rationale")

    return errors


def validate_pulse_package(
    stage_a: Dict[str, Any],
    stage_b: Dict[str, Any],
    corpus_ids: Set[str],
    sampled_ids: Set[str],
    id_to_text: Dict[str, str],
) -> Dict[str, Any]:
    """Full Phase 3 validation report."""
    a_errors = validate_stage_a(stage_a, sampled_ids)
    b_errors = validate_stage_b(stage_b, corpus_ids, id_to_text=id_to_text)
    theme_count = len(stage_a.get("themes", []))
    return {
        "valid": not a_errors and not b_errors,
        "stage_a_errors": a_errors,
        "stage_b_errors": b_errors,
        "theme_count": theme_count,
        "pulse_word_count": _word_count(stage_b.get("pulse_body", "")),
        "quote_count": len(stage_b.get("quotes", [])),
        "action_count": len(stage_b.get("actions", [])),
    }
