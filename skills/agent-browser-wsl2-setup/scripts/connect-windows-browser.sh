#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="windows-host"
BRIDGE_PORT="9333"

usage() {
  cat <<'EOF'
Usage:
  connect-windows-browser.sh [--session NAME] [--bridge-port PORT]
EOF
}

host_ip() {
  ip route | awk '/default/ {print $3; exit}'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)
      SESSION_NAME="$2"
      shift 2
      ;;
    --bridge-port)
      BRIDGE_PORT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

HOST_IP="$(host_ip)"

WS_URL="$(
  python3 - <<PY
import json, urllib.request
url = "http://${HOST_IP}:${BRIDGE_PORT}/json/version"
with urllib.request.urlopen(url, timeout=5) as resp:
    data = json.load(resp)
print(data["webSocketDebuggerUrl"])
PY
)"

agent-browser --session "${SESSION_NAME}" connect "${WS_URL}"
echo "Connected session ${SESSION_NAME} to ${HOST_IP}:${BRIDGE_PORT}"
