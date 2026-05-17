#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_SCRIPT="${SCRIPT_DIR}/setup-agent-browser-runtime.sh"
BROWSER_BRIDGE_SCRIPT="${SCRIPT_DIR}/../../wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh"
CONNECT_SCRIPT="${SCRIPT_DIR}/connect-windows-browser.sh"

CHECK_ONLY=0
SKIP_APT=0
SKIP_NPM=0
SKIP_BROWSER_INSTALL=0
SKIP_CLONE=0
SESSION_NAME="windows-host"
BROWSER_PORT="9223"
BRIDGE_PORT="9333"
START_URL="https://example.com"
REPO_DIR="${HOME}/src/agent-browser"

usage() {
  cat <<'EOF'
Usage:
  setup-agent-browser-wsl2.sh [options]

This is a compatibility wrapper around:
  1. setup-agent-browser-runtime.sh
  2. wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh
  3. connect-windows-browser.sh

Options:
  --check-only            Inspect and report, do not install or connect
  --skip-apt              Do not install apt packages
  --skip-npm              Do not install agent-browser
  --skip-browser-install  Do not run agent-browser install
  --skip-clone            Do not clone the GitHub repo
  --session NAME          agent-browser session name (default: windows-host)
  --browser-port PORT     Windows browser CDP port (default: 9223)
  --bridge-port PORT      Windows host bridge port visible to WSL2 (default: 9333)
  --start-url URL         URL to open in the host browser (default: https://example.com)
  --repo-dir PATH         Clone target for vercel-labs/agent-browser
EOF
}

run_runtime_setup() {
  local args=()

  [[ "${CHECK_ONLY}" -eq 1 ]] && args+=(--check-only)
  [[ "${SKIP_APT}" -eq 1 ]] && args+=(--skip-apt)
  [[ "${SKIP_NPM}" -eq 1 ]] && args+=(--skip-npm)
  [[ "${SKIP_BROWSER_INSTALL}" -eq 1 ]] && args+=(--skip-browser-install)
  [[ "${SKIP_CLONE}" -eq 1 ]] && args+=(--skip-clone)
  args+=(--repo-dir "${REPO_DIR}")

  bash "${RUNTIME_SCRIPT}" "${args[@]}"
}

run_bridge_setup() {
  local args=()

  [[ "${CHECK_ONLY}" -eq 1 ]] && args+=(--check-only)
  [[ "${SKIP_APT}" -eq 1 ]] && args+=(--skip-apt)
  args+=(--browser-port "${BROWSER_PORT}")
  args+=(--bridge-port "${BRIDGE_PORT}")
  args+=(--start-url "${START_URL}")

  bash "${BROWSER_BRIDGE_SCRIPT}" "${args[@]}"
}

print_summary() {
  cat <<EOF

Compatibility wrapper complete.

Next commands:
  agent-browser --session ${SESSION_NAME} get title
  agent-browser --session ${SESSION_NAME} snapshot -i -c
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check-only)
      CHECK_ONLY=1
      shift
      ;;
    --skip-apt)
      SKIP_APT=1
      shift
      ;;
    --skip-npm)
      SKIP_NPM=1
      shift
      ;;
    --skip-browser-install)
      SKIP_BROWSER_INSTALL=1
      shift
      ;;
    --skip-clone)
      SKIP_CLONE=1
      shift
      ;;
    --session)
      SESSION_NAME="$2"
      shift 2
      ;;
    --browser-port)
      BROWSER_PORT="$2"
      shift 2
      ;;
    --bridge-port)
      BRIDGE_PORT="$2"
      shift 2
      ;;
    --start-url)
      START_URL="$2"
      shift 2
      ;;
    --repo-dir)
      REPO_DIR="$2"
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

run_runtime_setup
run_bridge_setup

if [[ "${CHECK_ONLY}" -eq 1 ]]; then
  exit 0
fi

bash "${CONNECT_SCRIPT}" --session "${SESSION_NAME}" --bridge-port "${BRIDGE_PORT}"
print_summary
