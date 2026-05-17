#!/usr/bin/env bash
set -euo pipefail

CHECK_ONLY=0
SKIP_APT=0
SKIP_NPM=0
SKIP_BROWSER_INSTALL=0
SKIP_CLONE=0
REPO_DIR="${HOME}/src/agent-browser"

usage() {
  cat <<'EOF'
Usage:
  setup-agent-browser-runtime.sh [options]

Options:
  --check-only            Inspect and report only
  --skip-apt              Do not install apt packages
  --skip-npm              Do not install agent-browser
  --skip-browser-install  Do not run agent-browser install
  --skip-clone            Do not clone vercel-labs/agent-browser
  --repo-dir PATH         Clone target for vercel-labs/agent-browser
EOF
}

log() {
  printf '[agent-browser-runtime] %s\n' "$*"
}

fail() {
  printf '[agent-browser-runtime] ERROR: %s\n' "$*" >&2
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

install_agent_browser() {
  if have_cmd agent-browser; then
    log "agent-browser already installed"
    return
  fi

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_NPM}" -eq 1 ]]; then
    log "agent-browser is missing"
    return
  fi

  log "Installing agent-browser globally with npm"
  sudo npm install -g agent-browser
}

install_agent_browser_runtime() {
  if ! have_cmd agent-browser; then
    return
  fi

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_BROWSER_INSTALL}" -eq 1 ]]; then
    log "agent-browser install step is skipped"
    return
  fi

  log "Running agent-browser install"
  agent-browser install
}

clone_repo() {
  if [[ -d "${REPO_DIR}/.git" ]]; then
    log "agent-browser repo already present at ${REPO_DIR}"
    return
  fi

  if [[ "${CHECK_ONLY}" -eq 1 || "${SKIP_CLONE}" -eq 1 ]]; then
    log "agent-browser repo is missing at ${REPO_DIR}"
    return
  fi

  mkdir -p "$(dirname "${REPO_DIR}")"
  log "Cloning vercel-labs/agent-browser into ${REPO_DIR}"
  git clone https://github.com/vercel-labs/agent-browser "${REPO_DIR}"
}

report_agent_browser_version() {
  if have_cmd agent-browser; then
    log "agent-browser version: $(agent-browser --version)"
  fi
}

print_summary() {
  cat <<'EOF'

Runtime setup complete.

Next:
  1. Ensure a browser path already works via $wsl2-browser-setup
  2. For native WSL browsing, try:
       agent-browser doctor --offline --quick
       agent-browser open https://example.com
  3. For a Windows host bridge, attach with:
       bash "${CODEX_HOME:-$HOME/.codex}/skills/agent-browser-wsl2-setup/scripts/connect-windows-browser.sh"
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
    --repo-dir)
      REPO_DIR="$2"
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
queue_apt_if_missing git git
queue_apt_if_missing node nodejs
queue_apt_if_missing npm npm

install_apt_packages
install_agent_browser
install_agent_browser_runtime
clone_repo
report_agent_browser_version

if [[ "${CHECK_ONLY}" -eq 1 ]]; then
  exit 0
fi

print_summary
