#!/usr/bin/env bash
# Phase 1 helper (T1.4): scan for high-signal secret shapes. Not exhaustive.
# Markdown is excluded so docs that mention OAuth terms do not false-positive.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PATTERNS=(
  'AIza[0-9A-Za-z_-]{35}'
  'ya29\.[0-9A-Za-z_-]+'
  '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----'
  'xox[baprs]-[0-9A-Za-z-]+'
  'ghp_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]+'
)

scan_with_rg() {
  local found=0
  local p
  for p in "${PATTERNS[@]}"; do
    if rg --hidden --no-ignore-vcs -n -g '!**/*.md' -g '!.git/**' -g '!node_modules/**' "$p" . >/dev/null 2>&1; then
      echo "== Possible match for pattern: $p =="
      rg --hidden --no-ignore-vcs -n -g '!**/*.md' -g '!.git/**' -g '!node_modules/**' "$p" . || true
      found=1
    fi
  done
  return "$found"
}

scan_with_find_grep() {
  local found=0
  local p f
  while IFS= read -r -d '' f; do
    for p in "${PATTERNS[@]}"; do
      if grep -E "$p" "$f" >/dev/null 2>&1; then
        echo "== Possible match in $f for pattern: $p =="
        grep -nE "$p" "$f" || true
        found=1
      fi
    done
  done < <(find . \( -path './.git' -o -path './node_modules' \) -prune -o -type f ! -name '*.md' -print0)
  return "$found"
}

FOUND=0
if command -v rg >/dev/null 2>&1; then
  scan_with_rg || FOUND=1
else
  echo "Note: ripgrep (rg) not found; using find+grep fallback (slower)."
  scan_with_find_grep || FOUND=1
fi

if [[ "$FOUND" -ne 0 ]]; then
  echo ""
  echo "check-secrets: FAIL — review matches above."
  exit 1
fi

echo "check-secrets: OK — no high-signal matches (non-.md files scanned)."
exit 0
