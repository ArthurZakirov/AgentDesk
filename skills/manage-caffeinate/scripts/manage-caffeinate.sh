#!/usr/bin/env bash
set -euo pipefail

LABEL="agentdesk-caffeinate"
LEGACY_LABEL="codex-caffeinate"
CAFFEINATE="/usr/bin/caffeinate"

usage() {
  cat <<'EOF'
Usage:
  manage-caffeinate.sh on
  manage-caffeinate.sh off
  manage-caffeinate.sh status
  manage-caffeinate.sh restart
EOF
}

require_macos() {
  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This skill only supports macOS." >&2
    exit 1
  fi
}

is_loaded() {
  launchctl list "$1" >/dev/null 2>&1
}

managed_pids() {
  ps -axo pid=,command= | awk '
    $0 ~ /\/usr\/bin\/caffeinate -dimsu$/ {
      print $1
    }
  '
}

turn_on() {
  require_macos
  launchctl remove "${LEGACY_LABEL}" >/dev/null 2>&1 || true
  launchctl remove "${LABEL}" >/dev/null 2>&1 || true
  launchctl submit -l "${LABEL}" -- "${CAFFEINATE}" -dimsu
  echo "caffeinate is on via launchd job '${LABEL}'."
  status
}

turn_off() {
  require_macos
  local removed=0
  if is_loaded "${LABEL}"; then
    launchctl remove "${LABEL}"
    removed=1
  fi
  if is_loaded "${LEGACY_LABEL}"; then
    launchctl remove "${LEGACY_LABEL}"
    removed=1
  fi

  local pid
  for pid in $(managed_pids); do
    kill "${pid}" >/dev/null 2>&1 || true
    removed=1
  done

  if [[ "${removed}" -eq 1 ]]; then
    echo "caffeinate is off; removed managed launchd jobs and matching caffeinate processes."
  else
    echo "caffeinate is already off; no managed job or matching caffeinate process was found."
  fi
  status
}

status() {
  require_macos
  echo "launchd:"
  launchctl list "${LABEL}" 2>/dev/null || echo "  ${LABEL}: not loaded"
  launchctl list "${LEGACY_LABEL}" 2>/dev/null || echo "  ${LEGACY_LABEL}: not loaded"

  echo
  echo "managed processes:"
  local pids
  pids="$(managed_pids || true)"
  if [[ -n "${pids}" ]]; then
    ps -p "$(printf '%s\n' "${pids}" | paste -sd, -)" -o pid,stat,command
  else
    echo "  none"
  fi

  echo
  echo "power assertions:"
  pmset -g assertions | awk '
    /caffeinate/ || /PreventUserIdleSystemSleep/ || /PreventUserIdleDisplaySleep/ || /PreventSystemSleep/ {
      print
    }
  '
}

main() {
  case "${1:-}" in
    on|start|enable)
      turn_on
      ;;
    off|stop|disable)
      turn_off
      ;;
    status|check)
      status
      ;;
    restart)
      turn_off >/dev/null || true
      turn_on
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      echo "Unknown command: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
}

main "$@"
