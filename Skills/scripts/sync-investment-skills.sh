#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIRS=(
  "/Users/bella/.agents/skills"
  "/Users/bella/.codex/skills"
)
SKILLS=(
  "industry-understanding"
  "narrative-valuation"
  "investment-agent"
  "investment-market-opportunity-scanner"
  "investment-industry-value-chain"
  "investment-company-alpha"
  "investment-earnings-valuation"
  "investment-timing-portfolio"
  "investment-thesis-monitor"
  "investment-financial-statement-analysis"
)

MODE="${1:-sync}"
if [[ "$MODE" != "sync" && "$MODE" != "--check" ]]; then
  echo "usage: $0 [sync|--check]" >&2
  exit 2
fi

for skill in "${SKILLS[@]}"; do
  [[ -d "$SOURCE_DIR/$skill" ]] || {
    echo "missing source skill: $SOURCE_DIR/$skill" >&2
    exit 1
  }
done

if [[ "$MODE" == "sync" ]]; then
  for target in "${TARGET_DIRS[@]}"; do
    mkdir -p "$target"
    for skill in "${SKILLS[@]}"; do
      mkdir -p "$target/$skill"
      rsync -a --delete --exclude='.DS_Store' "$SOURCE_DIR/$skill/" "$target/$skill/"
    done
  done
fi

status=0
for target in "${TARGET_DIRS[@]}"; do
  for skill in "${SKILLS[@]}"; do
    if ! diff -qr --exclude='.DS_Store' "$SOURCE_DIR/$skill" "$target/$skill" >/dev/null; then
      echo "mismatch: $skill -> $target/$skill" >&2
      status=1
    fi
  done
done

if [[ "$status" -eq 0 ]]; then
  echo "research skill mirrors are consistent"
fi
exit "$status"
