"""Minimal Groq chat-completions client (stdlib only)."""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def parse_json_response(content: str) -> Dict[str, Any]:
    text = content.strip()
    if text.startswith("```"):
        text = FENCE_RE.sub("", text).strip()
    return json.loads(text)


def _retry_wait_seconds(detail: str, default: float = 60.0) -> float:
    match = re.search(r"try again in ([\d.]+)s", detail, re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1.0
    return default


def chat_json(
    *,
    api_key: str,
    system: str,
    user: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4096,
    max_attempts: int = 6,
) -> Dict[str, Any]:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "groww-weekly-pulse/1.0",
    }

    last_error: Optional[Exception] = None
    for attempt in range(max_attempts):
        req = urllib.request.Request(GROQ_API_URL, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            choice = payload["choices"][0]["message"]["content"]
            return parse_json_response(choice)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"Groq API HTTP {e.code}: {detail}")
            if e.code in (429, 413) and attempt < max_attempts - 1:
                wait = _retry_wait_seconds(detail, default=60.0 if e.code == 429 else 5.0)
                time.sleep(wait)
                continue
            raise last_error from e

    raise last_error or RuntimeError("Groq API failed after retries")


def pace(seconds: Optional[float] = None) -> None:
    delay = seconds if seconds is not None else float(os.environ.get("GROQ_PACE_SECONDS", "60"))
    if delay > 0:
        time.sleep(delay)


def require_api_key() -> str:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to .env (see .env.example).")
    return key
