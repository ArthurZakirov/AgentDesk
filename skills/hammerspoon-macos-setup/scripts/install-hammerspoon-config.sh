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

# Keep the logical invocation path. SkillPort may refresh the directory behind
# a stable installed-skill path, and the live symlinks should follow it.
script_dir="$(cd -L "$(dirname "${BASH_SOURCE[0]}")" && pwd -L)"
skill_dir="$(cd -L "${script_dir}/.." && pwd -L)"
source_dir="${skill_dir}/assets/hammerspoon"
target_dir="${HAMMERSPOON_CONFIG_DIR:-${HOME}/.hammerspoon}"

if [[ ! -d /Applications/Hammerspoon.app ]]; then
  brew install --cask hammerspoon
fi

if [[ ! -f "${source_dir}/init.lua" || ! -d "${source_dir}/modules" ]]; then
  printf 'Bundled Hammerspoon configuration is incomplete: %s\n' "${source_dir}" >&2
  exit 1
fi

linked_init=""
linked_modules=""
[[ -L "${target_dir}/init.lua" ]] && linked_init="$(readlink "${target_dir}/init.lua")"
[[ -L "${target_dir}/modules" ]] && linked_modules="$(readlink "${target_dir}/modules")"

if [[ "${linked_init}" != "${source_dir}/init.lua" || "${linked_modules}" != "${source_dir}/modules" ]]; then
  backup_root="${HOME}/.hammerspoon-backups"
  backup_dir="${backup_root}/$(date +%Y%m%d-%H%M%S)"
  mkdir -p "${backup_root}"
  if [[ -e "${target_dir}" ]]; then
    cp -R "${target_dir}" "${backup_dir}"
    printf 'Backed up the existing configuration to %s\n' "${backup_dir}"
  fi

  mkdir -p "${target_dir}"
  rm -f "${target_dir}/init.lua"
  rm -rf "${target_dir}/modules"
  ln -s "${source_dir}/init.lua" "${target_dir}/init.lua"
  ln -s "${source_dir}/modules" "${target_dir}/modules"
fi

if [[ "${HAMMERSPOON_SKIP_LAUNCH:-0}" != "1" ]]; then
  open -a Hammerspoon
  sleep 1
  if [[ -x /opt/homebrew/bin/hs ]]; then
    /opt/homebrew/bin/hs -c 'hs.reload()' >/dev/null 2>&1 || true
  fi
fi
printf 'Linked the live Hammerspoon configuration to %s\n' "${source_dir}"
printf 'Repository or SkillPort refreshes now update the live source; reload Hammerspoon to apply changes.\n'
printf 'If Accessibility is disabled, enable Hammerspoon in System Settings and restart the app.\n'
