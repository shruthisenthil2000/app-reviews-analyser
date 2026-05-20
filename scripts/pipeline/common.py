"""Shared utilities for corpus analysis and Stage 0 sampling."""
from __future__ import annotations

import csv
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

TOKEN_FACTOR = 1.3
ELLIPSIS = "\u2026"
ROOT = Path(__file__).resolve().parents[2]


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from .env into os.environ (existing vars are not overwritten)."""
    env_path = path or (ROOT / ".env")
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)

TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "trading": [
        "trading", "f&o", "option", "futures", "intraday", "stop loss", "order",
        "sell", "buy", "position", "margin", "limit order", "execution", "slippage",
    ],
    "app_stability_ux": [
        "crash", "bug", "slow", "lag", "hang", "not working", "freeze", "glitch",
        "loading", "error", "not opening", "not responding", "ui", "interface",
        "user friendly", "update",
    ],
    "withdrawals_payments": [
        "withdraw", "withdrawal", "payment", "bank", "transfer", "credit", "debit",
        "payout", "pending", "stuck", "money", "amount", "refund",
    ],
    "mutual_funds": [
        "mutual fund", "mutual funds", "sip", "external funds", "nav", "portfolio",
        "scheme", "redemption", "switch", "elss", "lumpsum",
    ],
    "brokerage_charges": [
        "brokerage", "charges", "fees", "commission", "hidden charges", "too much",
        "overcharge", "dp charges", "stt", "gst", "tax",
    ],
    "charts_data": [
        "chart", "candlestick", "indicator", "technical", "graph", "screener",
        "watchlist", "alert", "notification", "market data", "showing", "not showing",
    ],
    "customer_support": [
        "customer support", "customer care", "customer service", "support team",
        "helpline", "call", "response", "ticket", "resolve", "complaint",
    ],
    "account_kyc": [
        "account", "kyc", "verification", "demat", "login", "otp", "password",
        "locked", "blocked", "nominee", "pan",
    ],
}


@dataclass(frozen=True)
class ReviewRow:
    review_id: str
    rating: int
    title: str
    text: str
    date: str
    source_store: str

    @property
    def iso_week(self) -> str:
        d = date.fromisoformat(self.date)
        iso = d.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def tier(self) -> str:
        if self.rating <= 2:
            return "negative"
        if self.rating == 3:
            return "neutral"
        return "positive"


def load_reviews_csv(path: Path) -> List[ReviewRow]:
    rows: List[ReviewRow] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            rows.append(
                ReviewRow(
                    review_id=raw["review_id"].strip(),
                    rating=int(raw["rating"]),
                    title=(raw.get("title") or "").strip(),
                    text=(raw.get("text") or "").strip(),
                    date=raw["date"].strip(),
                    source_store=(raw.get("source_store") or "").strip(),
                )
            )
    return rows


def estimate_tokens(word_count: int) -> int:
    return int(word_count * TOKEN_FACTOR)


def truncate_text(text: str, max_chars: int) -> str:
    if max_chars < 4:
        raise ValueError("max_chars too small for truncation")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + ELLIPSIS


def stride_subsample(sorted_ids: List[str], cap: int) -> List[str]:
    if cap <= 0:
        return []
    if len(sorted_ids) <= cap:
        return list(sorted_ids)
    step = len(sorted_ids) / cap
    return [sorted_ids[int(i * step)] for i in range(cap)]


def topic_hits(text_lower: str) -> List[str]:
    hits = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            hits.append(topic)
    return hits


def top_bigrams(texts: Iterable[str], limit: int = 20) -> List[Tuple[str, int]]:
    counter: Counter[str] = Counter()
    word_re = re.compile(r"[a-z0-9']+")
    for text in texts:
        words = word_re.findall(text.lower())
        for i in range(len(words) - 1):
            counter[f"{words[i]} {words[i + 1]}"] += 1
    return counter.most_common(limit)


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
