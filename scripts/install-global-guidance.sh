#!/usr/bin/env sh
set -eu

repo="${AGENTDESK_REPOSITORY:-ArthurZakirov/AgentDesk}"
ref="${AGENTDESK_REF:-main}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
archive_url="${AGENTDESK_ARCHIVE_URL:-https://codeload.github.com/${repo}/tar.gz/${ref}}"

for command in curl tar mktemp sed find head cp mv mkdir date basename rm; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Missing required command: $command" >&2
    exit 1
  }
done

tmp="$(mktemp -d "${TMPDIR:-/tmp}/agentdesk-guidance.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

archive="$tmp/agentdesk.tar.gz"
extract="$tmp/extract"
mkdir -p "$extract"
curl -fsSL "$archive_url" -o "$archive"
tar -xzf "$archive" -C "$extract"

root="$(find "$extract" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
preview="$root/tests/fixtures/agents-md-preview/macos"
source_tree="$codex_home/agentdesk-source"

[ -f "$preview/AGENTS.md" ] || {
  echo "Downloaded AgentDesk archive does not contain the generated macOS guidance fixture." >&2
  exit 1
}
[ -d "$preview/agents-md-references" ] || {
  echo "Downloaded AgentDesk archive does not contain agents-md-references." >&2
  exit 1
}
[ -d "$root/global-guidance" ] || {
  echo "Downloaded AgentDesk archive does not contain global-guidance sources." >&2
  exit 1
}
[ -d "$root/scripts" ] || {
  echo "Downloaded AgentDesk archive does not contain scripts." >&2
  exit 1
}

mkdir -p "$codex_home"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup="$codex_home/guidance-backups/$stamp"

if [ -e "$codex_home/AGENTS.md" ] || [ -d "$codex_home/agents-md-references" ] || [ -d "$source_tree" ]; then
  mkdir -p "$backup"
  [ ! -e "$codex_home/AGENTS.md" ] || cp "$codex_home/AGENTS.md" "$backup/AGENTS.md"
  [ ! -d "$codex_home/agents-md-references" ] || cp -R "$codex_home/agents-md-references" "$backup/agents-md-references"
  [ ! -d "$source_tree" ] || cp -R "$source_tree" "$backup/agentdesk-source"
fi

stage="$tmp/stage"
mkdir -p "$stage/agents-md-references" "$stage/agentdesk-source"
cp "$preview/AGENTS.md" "$stage/AGENTS.md"
cp "$preview/agents-md-references/"* "$stage/agents-md-references/"
cp -R "$root/global-guidance" "$stage/agentdesk-source/global-guidance"
cp -R "$root/scripts" "$stage/agentdesk-source/scripts"

sed "s#<../../../../#<agentdesk-source/#g; s#\*\*AGENTS.md absolute path:\*\* \`<preview>/AGENTS.md\`#**AGENTS.md absolute path:** \`${codex_home}/AGENTS.md\`#" \
  "$stage/AGENTS.md" > "$stage/AGENTS.md.patched"
mv "$stage/AGENTS.md.patched" "$stage/AGENTS.md"

cp "$stage/AGENTS.md" "$codex_home/AGENTS.md.new"
mv "$codex_home/AGENTS.md.new" "$codex_home/AGENTS.md"
mkdir -p "$codex_home/agents-md-references"
for source in "$stage/agents-md-references/"*; do
  name="$(basename "$source")"
  cp "$source" "$codex_home/agents-md-references/$name.new"
  mv "$codex_home/agents-md-references/$name.new" "$codex_home/agents-md-references/$name"
done

rm -rf "$source_tree.new"
mv "$stage/agentdesk-source" "$source_tree.new"
rm -rf "$source_tree"
mv "$source_tree.new" "$source_tree"

printf '%s\n' "Installed AgentDesk guidance and local sources from ${repo}@${ref} into ${codex_home}."
if [ -d "$backup" ]; then
  printf '%s\n' "Previous guidance backed up to ${backup}."
fi
