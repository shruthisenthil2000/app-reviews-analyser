"""Render pulse text and MCP-ready delivery payloads."""
from __future__ import annotations

from typing import Any, Dict


def render_pulse_plain(stage_b: Dict[str, Any], week_label: str) -> str:
    lines = [f"Weekly App Review Pulse — Groww — {week_label}", ""]
    lines.append(stage_b.get("pulse_body", "").strip())
    lines.append("")
    lines.append("User voices (paraphrased)")
    for i, q in enumerate(stage_b.get("quotes", []), 1):
        lines.append(f'{i}. "{q.get("text", "").strip()}"')
    lines.append("")
    lines.append("Suggested actions")
    for i, a in enumerate(stage_b.get("actions", []), 1):
        lines.append(f"{i}. {a.get('title', '').strip()} — {a.get('rationale', '').strip()}")
    return "\n".join(lines) + "\n"


def build_mcp_delivery(
    stage_b: Dict[str, Any],
    *,
    week_label: str,
    to_email: str,
    doc_id: str = "",
) -> Dict[str, Any]:
    subject = f"Groww Play Store Pulse — {week_label}"
    body = render_pulse_plain(stage_b, week_label)
    return {
        "week_label": week_label,
        "gmail": {
            "tool": "create_email_draft",
            "to": to_email,
            "subject": subject,
            "body": body,
        },
        "docs": {
            "tool": "append_to_doc",
            "doc_id": doc_id,
            "content": body,
        },
        "plain_text": body,
    }
