#!/usr/bin/env python3
"""
Deliver pulse via Saksham MCP (thin wrapper around pipeline.mcp_deliver).

Prefer: python3 scripts/run_phase4.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.finalize import finalize_phase3_run  # noqa: E402
from scripts.pipeline.mcp_client import list_tools, mcp_base_url  # noqa: E402
from scripts.pipeline.mcp_deliver import (  # noqa: E402
    DeliveryConfig,
    deliver_pulse,
    load_config_from_env,
    write_delivery_manifest,
)


def main() -> int:
    config = load_config_from_env()
    parser = argparse.ArgumentParser(description="Deliver pulse via Saksham MCP HTTP API.")
    parser.add_argument("--docs", action="store_true")
    parser.add_argument("--gmail", action="store_true")
    parser.add_argument("--all", action="store_true", help="Gmail + Docs (default if flags omitted)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    if args.list_tools:
        import json

        print(json.dumps(list_tools(), indent=2))
        return 0

    if args.refresh:
        finalize_phase3_run(to_email=config.to_email, doc_id=config.doc_id)

    if args.docs:
        config.deliver_gmail = False
        config.deliver_docs = True
    elif args.gmail:
        config.deliver_gmail = True
        config.deliver_docs = False
    else:
        config.deliver_gmail = True
        config.deliver_docs = bool(config.doc_id)

    config.dry_run = args.dry_run
    print(f"MCP server: {mcp_base_url()}")
    result = deliver_pulse(config)
    write_delivery_manifest(result, config)
    if not result.ok:
        for e in result.errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("Delivery complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
