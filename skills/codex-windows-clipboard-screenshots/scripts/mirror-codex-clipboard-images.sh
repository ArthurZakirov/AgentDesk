#!/usr/bin/env bash
set -euo pipefail

task_work_dir="${1:-work}"
source_dir="/mnt/c/Users/arthu/AppData/Local/Temp"
target_dir="$task_work_dir/clipboard-images"
latest_link="$target_dir/latest.png"

mkdir -p "$target_dir"

while true; do
  newest_source="$(
    find "$source_dir" -maxdepth 1 -type f -name 'codex-clipboard-*.png' -printf '%T@ %p\n' 2>/dev/null \
      | sort -n \
      | tail -1 \
      | cut -d' ' -f2-
  )"

  for file in "$source_dir"/codex-clipboard-*.png; do
    [ -e "$file" ] || continue
    cp -p "$file" "$target_dir/$(basename "$file")" 2>/dev/null || true
  done

  if [ -n "$newest_source" ]; then
    latest="$target_dir/$(basename "$newest_source")"
    ln -sfn "$latest" "$latest_link"
  fi

  sleep 1
done
