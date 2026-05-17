#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_PATH="${HOME}/.config/AgentDesk/personal-profile.yaml"
TARGET="${ADC_PERSONAL_PROFILE_PATH:-${DEFAULT_PATH}}"

mkdir -p "$(dirname "${TARGET}")"

if [[ -e "${TARGET}" ]]; then
  echo "Profile already exists: ${TARGET}" >&2
  exit 0
fi

cp "${SKILL_DIR}/references/personal-profile.example.yaml" "${TARGET}"
chmod 600 "${TARGET}" || true

cat <<EOF
Created private profile template:
${TARGET}

Edit this file with real values. Do not commit it to Git.
To make the path explicit for agents, add this to your shell profile:

export ADC_PERSONAL_PROFILE_PATH="${TARGET}"
EOF
