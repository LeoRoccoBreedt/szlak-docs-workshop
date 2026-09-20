#!/usr/bin/env bash
# Validate the documentation: links, includes, and STYLE.md rules.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 build.py
