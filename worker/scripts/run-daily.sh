#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
MODE_FLAG=()
LIVE_FLAG=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --live) LIVE_FLAG=(--live); shift ;;
    --mode) MODE_FLAG=(--mode "$2"); shift 2 ;;
    *) shift ;;
  esac
done
python -m passive_income_ideas run-daily "${LIVE_FLAG[@]}" "${MODE_FLAG[@]}"
