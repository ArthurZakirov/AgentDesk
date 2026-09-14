#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  printf 'Python 3 is required to install the device guard.\n' >&2
  exit 1
fi
exec python3 "${SCRIPT_DIR}/install-device-macos.py" "$@"
