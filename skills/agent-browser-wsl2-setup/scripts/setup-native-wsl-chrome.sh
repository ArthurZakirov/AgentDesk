#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${SCRIPT_DIR}/../../wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh"

if [[ ! -f "${TARGET}" ]]; then
  echo "Missing delegated script: ${TARGET}" >&2
  exit 1
fi

echo "[agent-browser-wsl2-setup] Delegating native Chrome setup to wsl2-browser-setup"
exec bash "${TARGET}" "$@"
