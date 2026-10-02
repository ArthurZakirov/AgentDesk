#!/usr/bin/env zsh
set -euo pipefail

LABEL="com.agentdesk.codex-langsmith-env"
TARGET_ENV="LANGSMITH_CODEX_API_KEY"
RUNTIME_DIR="${HOME}/.local/libexec/agentdesk"
RUNTIME_PATH="${RUNTIME_DIR}/manage-codex-langsmith-env.sh"
PLIST_PATH="${HOME}/Library/LaunchAgents/${LABEL}.plist"
SELF_PATH="${0:A}"

usage() {
  cat <<'EOF'
Usage:
  BWS_KEYCHAIN_ACCOUNT=<account> manage-codex-langsmith-env.sh install
  manage-codex-langsmith-env.sh refresh
  manage-codex-langsmith-env.sh status
  manage-codex-langsmith-env.sh uninstall

Optional install setting:
  BWS_KEYCHAIN_SERVICE  macOS Keychain service name (default: BWS_ACCESS_TOKEN)

The Bitwarden secret must be named LANGSMITH_API_KEY.
Secret values are never printed or written to disk.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

gui_domain() {
  printf 'gui/%s' "$(/usr/bin/id -u)"
}

status() {
  local domain
  domain="$(gui_domain)"

  if /bin/launchctl print "${domain}/${LABEL}" >/dev/null 2>&1; then
    printf 'LaunchAgent: loaded\n'
  else
    printf 'LaunchAgent: not loaded\n'
  fi

  if [[ -n "$(/bin/launchctl getenv "${TARGET_ENV}" 2>/dev/null)" ]]; then
    printf '%s: present (value hidden)\n' "${TARGET_ENV}"
  else
    printf '%s: absent\n' "${TARGET_ENV}"
  fi
}

run_refresh() {
  : "${BWS_BIN:?BWS_BIN is required}"
  : "${BWS_KEYCHAIN_ACCOUNT:?BWS_KEYCHAIN_ACCOUNT is required}"
  : "${BWS_KEYCHAIN_SERVICE:?BWS_KEYCHAIN_SERVICE is required}"

  local bws_access_token
  bws_access_token="$(
    /usr/bin/security find-generic-password \
      -a "${BWS_KEYCHAIN_ACCOUNT}" \
      -s "${BWS_KEYCHAIN_SERVICE}" \
      -w 2>/dev/null
  )" || exit 10
  [[ -n "${bws_access_token}" ]] || exit 11
  export BWS_ACCESS_TOKEN="${bws_access_token}"

  set +e
  "${BWS_BIN}" run --no-inherit-env --output none -- /bin/zsh -c '
    [[ -n "${LANGSMITH_API_KEY:-}" ]] || exit 20
    /bin/launchctl setenv LANGSMITH_CODEX_API_KEY "${LANGSMITH_API_KEY}"
  ' >/dev/null 2>&1
  local rc=$?
  set -e

  unset BWS_ACCESS_TOKEN
  bws_access_token=""
  return "${rc}"
}

write_plist() {
  local bws_bin="$1"
  local keychain_account="$2"
  local keychain_service="$3"

  /bin/mkdir -p "${HOME}/Library/LaunchAgents"
  /bin/chmod 700 "${HOME}/Library/LaunchAgents" 2>/dev/null || true

  cat >"${PLIST_PATH}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${RUNTIME_PATH}</string>
    <string>run</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>BWS_BIN</key>
    <string>${bws_bin}</string>
    <key>BWS_KEYCHAIN_ACCOUNT</key>
    <string>${keychain_account}</string>
    <key>BWS_KEYCHAIN_SERVICE</key>
    <string>${keychain_service}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>60</integer>
  <key>ProcessType</key>
  <string>Background</string>
  <key>StandardOutPath</key>
  <string>/dev/null</string>
  <key>StandardErrorPath</key>
  <string>/dev/null</string>
</dict>
</plist>
EOF

  /bin/chmod 600 "${PLIST_PATH}"
  /usr/bin/plutil -lint "${PLIST_PATH}" >/dev/null
}

install_agent() {
  local keychain_account="${BWS_KEYCHAIN_ACCOUNT:-}"
  local keychain_service="${BWS_KEYCHAIN_SERVICE:-BWS_ACCESS_TOKEN}"
  [[ -n "${keychain_account}" ]] || die "set BWS_KEYCHAIN_ACCOUNT for the existing Keychain item"

  local bws_bin
  bws_bin="$(command -v bws || true)"
  [[ -x "${bws_bin}" ]] || die "bws CLI was not found"

  /bin/mkdir -p "${RUNTIME_DIR}"
  /bin/chmod 700 "${RUNTIME_DIR}"
  /usr/bin/install -m 700 "${SELF_PATH}" "${RUNTIME_PATH}"

  write_plist "${bws_bin}" "${keychain_account}" "${keychain_service}"

  local domain
  domain="$(gui_domain)"
  /bin/launchctl bootout "${domain}/${LABEL}" >/dev/null 2>&1 || true
  /bin/launchctl bootstrap "${domain}" "${PLIST_PATH}"

  /bin/sleep 1
  status
}

refresh_agent() {
  local domain
  domain="$(gui_domain)"
  /bin/launchctl print "${domain}/${LABEL}" >/dev/null 2>&1 \
    || die "LaunchAgent is not loaded; run install first"

  /bin/launchctl bootout "${domain}/${LABEL}" >/dev/null 2>&1 || true
  /bin/launchctl unsetenv "${TARGET_ENV}" >/dev/null 2>&1 || true
  /bin/launchctl bootstrap "${domain}" "${PLIST_PATH}"

  /bin/sleep 1
  status
}

uninstall_agent() {
  local domain
  domain="$(gui_domain)"

  /bin/launchctl bootout "${domain}/${LABEL}" >/dev/null 2>&1 || true
  /bin/launchctl unsetenv "${TARGET_ENV}" >/dev/null 2>&1 || true
  /bin/rm -f "${PLIST_PATH}" "${RUNTIME_PATH}"
  /bin/rmdir "${RUNTIME_DIR}" >/dev/null 2>&1 || true

  printf 'LaunchAgent removed; %s unset.\n' "${TARGET_ENV}"
}

action="${1:-status}"
case "${action}" in
  install)
    install_agent
    ;;
  refresh)
    refresh_agent
    ;;
  status)
    status
    ;;
  uninstall)
    uninstall_agent
    ;;
  run)
    run_refresh
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
