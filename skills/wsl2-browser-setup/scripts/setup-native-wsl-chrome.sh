#!/usr/bin/env bash
set -euo pipefail

CHECK_ONLY=0
SKIP_APT=0
SKIP_CHROME_INSTALL=0
SKIP_WSLCONFIG=0

usage() {
  cat <<'EOF'
Usage:
  setup-native-wsl-chrome.sh [options]

Options:
  --check-only          Inspect and report only
  --skip-apt            Do not install apt packages
  --skip-chrome-install Do not install google-chrome
  --skip-wslconfig      Do not write .wslconfig
EOF
}

log() {
  printf '[wsl2-browser-setup:native] %s\n' "$*"
}

fail() {
  printf '[wsl2-browser-setup:native] ERROR: %s\n' "$*" >&2
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

install_google_chrome() {
  if have_cmd google-chrome; then
    log "google-chrome already installed"
    return
  fi

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_CHROME_INSTALL}" -eq 1 ]]; then
    log "google-chrome is missing"
    return
  fi

  local deb="/tmp/google-chrome-stable_current_amd64.deb"
  log "Downloading Google Chrome .deb"
  curl -fsSL -o "${deb}" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  log "Installing Google Chrome"
  sudo apt-get install -y "${deb}"
}

ensure_wslconfig() {
  local script_win
  script_win="$(wslpath -w "${SCRIPT_DIR}/ensure-wslconfig.ps1")"

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_WSLCONFIG}" -eq 1 ]]; then
    log ".wslconfig step is skipped"
    return
  fi

  log "Writing Windows .wslconfig for mirrored networking and dnsTunneling"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "${script_win}"
}

report_wslconfig() {
  local win_home wslconfig
  win_home="$(powershell.exe -NoProfile -Command '$HOME' 2>/dev/null | tr -d '\r')"
  if [[ -n "${win_home}" ]]; then
    wslconfig="$(wslpath "${win_home}\\.wslconfig" 2>/dev/null || true)"
    if [[ -n "${wslconfig}" && -f "${wslconfig}" ]]; then
      log ".wslconfig present at ${wslconfig}"
    else
      log ".wslconfig is missing"
    fi
  fi
}

report_chrome_version() {
  if have_cmd google-chrome; then
    log "google-chrome version: $(google-chrome --version)"
  fi
}

print_restart_note() {
  cat <<'EOF'

If .wslconfig was changed or created, the human must now run:
  wsl --shutdown

Then reopen WSL, launch:
  google-chrome

In Chrome:
  1. Open chrome://settings/security
  2. Turn "Use secure DNS" fully Off
  3. Reopen Chrome
  4. Test https://example.com and one normal external HTTPS site
  5. Test the target sign-in page or app you need
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
    --skip-chrome-install)
      SKIP_CHROME_INSTALL=1
      shift
      ;;
    --skip-wslconfig)
      SKIP_WSLCONFIG=1
      shift
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
install_google_chrome
ensure_wslconfig

report_wslconfig
report_chrome_version

if [[ "${CHECK_ONLY}" -eq 1 ]]; then
  exit 0
fi

print_restart_note
