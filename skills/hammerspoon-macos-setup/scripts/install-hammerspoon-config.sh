#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  printf 'This installer supports macOS only.\n' >&2
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  printf 'Homebrew is required to install Hammerspoon.\n' >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "${script_dir}/.." && pwd)"
source_dir="${skill_dir}/assets/hammerspoon"
target_dir="${HOME}/.hammerspoon"

if [[ ! -d /Applications/Hammerspoon.app ]]; then
  brew install --cask hammerspoon
fi

if [[ -e "${target_dir}" ]]; then
  backup_root="${HOME}/.hammerspoon-backups"
  backup_dir="${backup_root}/$(date +%Y%m%d-%H%M%S)"
  mkdir -p "${backup_root}"
  cp -R "${target_dir}" "${backup_dir}"
  printf 'Backed up the existing configuration to %s\n' "${backup_dir}"
fi

mkdir -p "${target_dir}/modules"
cp "${source_dir}/init.lua" "${target_dir}/init.lua"
cp "${source_dir}/modules/"*.lua "${target_dir}/modules/"

open -a Hammerspoon
sleep 1
if [[ -x /opt/homebrew/bin/hs ]]; then
  /opt/homebrew/bin/hs -c 'hs.reload()' >/dev/null 2>&1 || true
fi
printf 'Installed the modular Hammerspoon configuration in %s\n' "${target_dir}"
printf 'If Accessibility is disabled, enable Hammerspoon in System Settings and restart the app.\n'
