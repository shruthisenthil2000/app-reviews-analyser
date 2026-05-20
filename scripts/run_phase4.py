#!/usr/bin/env python3
"""
Phase 4: Deliver weekly pulse via Saksham Google MCP server (Gmail draft + optional Docs).

Requires Phase 3 artifacts (validated pulse). Configure .env:

  MCP_SERVER_URL=https://saksham-mcp-server-production-f2a5.up.railway.app
  PULSE_TO_EMAIL=you@example.com
  GOOGLE_DOC_ID=...          # optional but recommended

Usage:
  python3 scripts/run_phase4.py
  python3 scripts/run_phase4.py --dry-run
  python3 scripts/run_phase4.py --gmail-only
  python3 scripts/run_phase4.py --docs-only
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.common import load_dotenv  # noqa: E402
from scripts.pipeline.finalize import finalize_phase3_run  # noqa: E402
from scripts.pipeline.mcp_deliver import (  # noqa: E402
    DeliveryConfig,
    deliver_pulse,
    load_config_from_env,
    write_delivery_manifest,
)


def main() -> int:
    load_dotenv()
    config = load_config_from_env()

    parser = argparse.ArgumentParser(description="Phase 4: MCP delivery (Gmail + Docs).")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without calling MCP")
    parser.add_argument("--gmail-only", action="store_true")
    parser.add_argument("--docs-only", action="store_true")
    parser.add_argument("--skip-validate", action="store_true", help="Skip Phase 3 validate_pulse check")
    parser.add_argument("--no-refresh", action="store_true", help="Do not rebuild mcp_delivery.json")
    args = parser.parse_args()

    if args.gmail_only:
        config.deliver_docs = False
    elif args.docs_only:
        config.deliver_gmail = False
    config.dry_run = args.dry_run

    if not args.skip_validate:
        print("== Phase 4: validating Phase 3 pulse ==")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_pulse.py")],
            cwd=ROOT,
        )
        if proc.returncode != 0:
            print("ERROR: pulse validation failed — fix Phase 3 before delivery", file=sys.stderr)
            return 1

    if not args.no_refresh:
        print("== Phase 4: refreshing mcp_delivery.json from .env ==")
        finalize_phase3_run(to_email=config.to_email, doc_id=config.doc_id)

    if config.deliver_gmail and not config.to_email:
        print(
            "ERROR: Set PULSE_TO_EMAIL in .env (recipient for Gmail draft).\n"
            "  Example: PULSE_TO_EMAIL=your.name@gmail.com\n"
            "  Or use --docs-only to skip Gmail.",
            file=sys.stderr,
        )
        return 1

    if not config.deliver_gmail and not config.deliver_docs:
        print("ERROR: nothing to deliver", file=sys.stderr)
        return 1

    print(f"== Phase 4: MCP delivery ({'dry-run' if config.dry_run else 'live'}) ==")
    if config.deliver_gmail:
        print(f"  Gmail → {config.to_email}")
    if config.deliver_docs and config.doc_id:
        print(f"  Docs  → {config.doc_id[:12]}…")

    result = deliver_pulse(config)
    manifest_path = write_delivery_manifest(result, config)

    if result.gmail:
        print("Gmail:", result.gmail)
    if result.docs:
        print("Docs:", result.docs)
    if result.errors:
        for err in result.errors:
            print(f"ERROR: {err}", file=sys.stderr)

    print(f"Manifest: {manifest_path}")
    if result.ok and not config.dry_run and config.deliver_gmail:
        print("\nNext: open Gmail → Drafts and confirm formatting before sending.")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
