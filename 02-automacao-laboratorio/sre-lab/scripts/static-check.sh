#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 -m py_compile scripts/*.py
for file in scripts/*.sh; do bash -n "$file"; done
if command -v ruby >/dev/null; then ruby -c vagrant/Vagrantfile; else echo 'SKIP Ruby ausente'; fi
python3 -m unittest discover -s tests -v
make -n install validate start stop ssh NODE=master-1
