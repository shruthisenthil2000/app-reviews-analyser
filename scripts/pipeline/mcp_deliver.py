"""Phase 4 delivery orchestration (Saksham MCP HTTP — no googleapis in-repo)."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from scripts.pipeline.common import ROOT, load_dotenv, utc_now_iso
from scripts.pipeline.mcp_client import append_to_doc, create_email_draft, mcp_base_url

ARTIFACTS = ROOT / "artifacts"
DELIVERY_PATH = ARTIFACTS / "mcp_delivery.json"
RUNS_P4 = ROOT / "runs/phase-04"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class DeliveryConfig:
    to_email: str = ""
    doc_id: str = ""
    dry_run: bool = False
    deliver_gmail: bool = True
    deliver_docs: bool = True


@dataclass
class DeliveryResult:
    ok: bool
    gmail: Optional[Dict[str, Any]] = None
    docs: Optional[Dict[str, Any]] = None
    errors: List[str] = field(default_factory=list)


def load_config_from_env() -> DeliveryConfig:
    load_dotenv()
    return DeliveryConfig(
        to_email=os.environ.get("PULSE_TO_EMAIL", "").strip(),
        doc_id=os.environ.get("GOOGLE_DOC_ID", "").strip(),
    )


def validate_email(address: str) -> Optional[str]:
    if not address:
        return "PULSE_TO_EMAIL is not set in .env"
    if not EMAIL_RE.match(address):
        return f"PULSE_TO_EMAIL looks invalid: {address!r}"
    return None


def load_delivery_payload() -> Dict[str, Any]:
    if not DELIVERY_PATH.is_file():
        raise FileNotFoundError(
            f"Missing {DELIVERY_PATH}. Run: python3 scripts/run_phase3.py --skip-groq --validate-only"
        )
    return json.loads(DELIVERY_PATH.read_text(encoding="utf-8"))


def apply_env_to_delivery(delivery: Dict[str, Any], config: DeliveryConfig) -> Dict[str, Any]:
    out = json.loads(json.dumps(delivery))
    if config.to_email:
        out.setdefault("gmail", {})["to"] = config.to_email
    if config.doc_id:
        out.setdefault("docs", {})["doc_id"] = config.doc_id
    return out


def deliver_pulse(config: DeliveryConfig, delivery: Optional[Dict[str, Any]] = None) -> DeliveryResult:
    payload = apply_env_to_delivery(delivery or load_delivery_payload(), config)
    result = DeliveryResult(ok=True)

    if config.deliver_gmail:
        err = validate_email(config.to_email or payload.get("gmail", {}).get("to", ""))
        if err:
            result.errors.append(err)
            result.ok = False
        else:
            g = payload["gmail"]
            to, subject, body = g["to"], g["subject"], g["body"]
            if not body.strip():
                result.errors.append("Gmail body is empty")
                result.ok = False
            elif config.dry_run:
                result.gmail = {
                    "status": "dry_run",
                    "to": to,
                    "subject": subject,
                    "body_chars": len(body),
                }
            else:
                result.gmail = create_email_draft(to, subject, body)
                if result.gmail.get("status") != "success":
                    result.errors.append(
                        result.gmail.get("message") or "Gmail draft creation failed"
                    )
                    result.ok = False

    if config.deliver_docs:
        doc_id = config.doc_id or payload.get("docs", {}).get("doc_id", "")
        if not doc_id:
            if config.deliver_gmail:
                result.docs = {"status": "skipped", "message": "GOOGLE_DOC_ID not set"}
            else:
                result.errors.append("GOOGLE_DOC_ID is not set in .env")
                result.ok = False
        else:
            content = payload.get("docs", {}).get("content") or payload.get("plain_text", "")
            if not content.strip():
                result.errors.append("Doc content is empty")
                result.ok = False
            elif config.dry_run:
                result.docs = {
                    "status": "dry_run",
                    "document_id": doc_id,
                    "content_chars": len(content),
                }
            else:
                result.docs = append_to_doc(doc_id, content)
                if result.docs.get("status") != "success":
                    result.errors.append(
                        result.docs.get("message") or "Google Doc append failed"
                    )
                    result.ok = False

    return result


def write_delivery_manifest(result: DeliveryResult, config: DeliveryConfig) -> Path:
    RUNS_P4.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1.0",
        "completed_at": utc_now_iso(),
        "mcp_server": mcp_base_url(),
        "dry_run": config.dry_run,
        "recipient_configured": bool(config.to_email),
        "doc_configured": bool(config.doc_id),
        "ok": result.ok,
        "gmail": _redact_result(result.gmail),
        "docs": _redact_result(result.docs),
        "errors": result.errors,
    }
    path = RUNS_P4 / "delivery_manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def _redact_result(block: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not block:
        return block
    out = dict(block)
    if "body" in out:
        out["body"] = f"<{len(out['body'])} chars omitted from log>"
    return out
