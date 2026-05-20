"""HTTP client for Saksham Google MCP server (REST, not googleapis in-repo)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

DEFAULT_BASE_URL = "https://saksham-mcp-server-production-f2a5.up.railway.app"


def mcp_base_url() -> str:
    return os.environ.get("MCP_SERVER_URL", DEFAULT_BASE_URL).rstrip("/")


def mcp_api_key() -> Optional[str]:
    return (
        os.environ.get("MCP_API_KEY")
        or os.environ.get("SAKSHAM_MCP_API_KEY")
        or os.environ.get("X_API_KEY")
        or None
    )


def _request(method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{mcp_base_url()}{path}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    key = mcp_api_key()
    if key:
        headers["X-API-Key"] = key
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {"status": "success"}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(detail)
        except json.JSONDecodeError:
            return {"status": "error", "message": detail, "http_status": e.code}


def list_tools() -> Any:
    return _request("GET", "/tools")


def append_to_doc(doc_id: str, content: str) -> Dict[str, Any]:
    return _request("POST", "/append_to_doc", {"doc_id": doc_id, "content": content})


def create_email_draft(to: str, subject: str, body: str) -> Dict[str, Any]:
    return _request("POST", "/create_email_draft", {"to": to, "subject": subject, "body": body})
