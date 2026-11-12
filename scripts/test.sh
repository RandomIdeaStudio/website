#!/usr/bin/env bash
# Runs every check of the website (Linux, cloud, CI). Same as scripts/test.ps1.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I scripts/check_site.py
