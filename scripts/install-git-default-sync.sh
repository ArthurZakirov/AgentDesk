#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SYNC_SCRIPT="$SCRIPT_DIR/sync-default-branch.py"

if [ ! -f "$SYNC_SCRIPT" ]; then
  echo "Missing $SYNC_SCRIPT" >&2
  exit 1
fi

chmod +x "$SYNC_SCRIPT"
git config --global alias.sync-default "!python3 '$SYNC_SCRIPT'"
echo "Installed: git sync-default [--remote <name>]"
