#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${1:-}" == "--help" ]]; then echo "Uso: recovery.sh [ID-da-sessão] — reinicia apenas exercício sintético"; exit 0; fi
if [[ $# -eq 1 ]]; then exec python3 "$ROOT/scripts/incident.py" --session "$1" recover; elif [[ $# -eq 0 ]]; then exec python3 "$ROOT/scripts/incident.py" recover; else exit 2; fi
