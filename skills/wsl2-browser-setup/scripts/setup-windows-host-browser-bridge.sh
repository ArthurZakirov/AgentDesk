#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CHECK_ONLY=0
SKIP_APT=0
BROWSER_PORT="9223"
BRIDGE_PORT="9333"
START_URL="https://example.com"

usage() {
  cat <<'EOF'
Usage:
  setup-windows-host-browser-bridge.sh [options]

Options:
  --check-only         Inspect and report, do not launch or change config
  --skip-apt           Do not install apt packages
  --browser-port PORT  Windows browser CDP port (default: 9223)
  --bridge-port PORT   Windows host bridge port visible to WSL2 (default: 9333)
  --start-url URL      URL to open in the host browser (default: https://example.com)
EOF
}

log() {
  printf '[wsl2-browser-setup:bridge] %s\n' "$*"
}

fail() {
  printf '[wsl2-browser-setup:bridge] ERROR: %s\n' "$*" >&2
  exit 1
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

require_wsl() {
  if [[ -z "${WSL_DISTRO_NAME:-}" ]] && ! grep -qi microsoft /proc/version 2>/dev/null; then
    fail "This script is intended for WSL/WSL2."
  fi
}

host_ip() {
  ip route | awk '/default/ {print $3; exit}'
}

need_apt=()

queue_apt_if_missing() {
  local cmd="$1"
  local pkg="$2"
  if ! have_cmd "${cmd}"; then
    need_apt+=("${pkg}")
  fi
}

install_apt_packages() {
  if [[ ${#need_apt[@]} -eq 0 ]]; then
    return
  fi

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_APT}" -eq 1 ]]; then
    log "Missing apt packages: ${need_apt[*]}"
    return
  fi

  log "Installing apt packages: ${need_apt[*]}"
  sudo apt-get update
  sudo apt-get install -y "${need_apt[@]}"
}

detect_windows_browser() {
  powershell.exe -NoProfile -Command '
    $candidates = @(
      "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
      "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
      "C:\Program Files\Google\Chrome\Application\chrome.exe",
      "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
    foreach ($candidate in $candidates) {
      if (Test-Path $candidate) {
        Write-Output $candidate
        exit 0
      }
    }
    exit 1
  ' 2>/dev/null
}

report_windows_browser() {
  local browser_path
  if browser_path="$(detect_windows_browser)"; then
    log "Windows host browser found: ${browser_path}"
  else
    log "No supported Windows host browser found"
  fi
}

report_bridge_status() {
  local ip
  ip="$(host_ip)"
  if curl -fsS "http://${ip}:${BRIDGE_PORT}/json/version" >/dev/null 2>&1; then
    log "Bridge is reachable at http://${ip}:${BRIDGE_PORT}/json/version"
  else
    log "Bridge is not reachable at http://${ip}:${BRIDGE_PORT}/json/version"
  fi
}

run_windows_browser_launch() {
  local ps1_win
  ps1_win="$(wslpath -w "${SCRIPT_DIR}/launch-host-browser.ps1")"
  log "Launching Windows host browser on port ${BROWSER_PORT}"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "${ps1_win}" \
    -BrowserPort "${BROWSER_PORT}" \
    -StartUrl "${START_URL}"
}

run_windows_bridge_setup() {
  local ps1_win
  ps1_win="$(wslpath -w "${SCRIPT_DIR}/invoke-portproxy-admin.ps1")"
  log "Requesting Windows elevation for port proxy and firewall rule"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "${ps1_win}" \
    -BrowserPort "${BROWSER_PORT}" \
    -BridgePort "${BRIDGE_PORT}"
}

wait_for_bridge() {
  local ip
  ip="$(host_ip)"
  log "Waiting for bridge at http://${ip}:${BRIDGE_PORT}/json/version"

  for _ in $(seq 1 30); do
    if curl -fsS "http://${ip}:${BRIDGE_PORT}/json/version" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  return 1
}

print_summary() {
  local ip
  ip="$(host_ip)"
  cat <<EOF

Bridge is ready.

Endpoint:
  http://${ip}:${BRIDGE_PORT}/json/version

Any CDP-capable client in WSL2 can now discover the browser websocket from that endpoint.
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
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Unknown argument: $1"
      ;;
  esac
done

require_wsl

queue_apt_if_missing curl curl

install_apt_packages
report_windows_browser

if [[ "${CHECK_ONLY}" -eq 1 ]]; then
  report_bridge_status
  exit 0
fi

run_windows_browser_launch
run_windows_bridge_setup

if ! wait_for_bridge; then
  fail "Bridge did not become reachable on port ${BRIDGE_PORT}"
fi

print_summary
