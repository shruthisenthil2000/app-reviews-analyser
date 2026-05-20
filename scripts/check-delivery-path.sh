#!/usr/bin/env bash
# Phase 4 (T4.4): ensure delivery uses MCP HTTP only, not googleapis in-repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PATTERNS=(
  'googleapis'
  'from google.oauth2'
  'googleapiclient'
)

FOUND=0
for pat in "${PATTERNS[@]}"; do
  if rg -n --glob 'scripts/**' --glob '!scripts/check-delivery-path.sh' "$pat" scripts/ 2>/dev/null; then
    FOUND=1
  fi
done

if [[ "$FOUND" -ne 0 ]]; then
  echo "check-delivery-path: FAIL — google API client usage in scripts/"
  exit 1
fi

echo "check-delivery-path: OK — delivery scripts use Saksham MCP HTTP only."
exit 0
