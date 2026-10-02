#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_CONFIG="$SCRIPT_DIR/../config/git/gitconfig"

if [ ! -f "$SOURCE_CONFIG" ]; then
  echo "Missing $SOURCE_CONFIG" >&2
  exit 1
fi

SOURCE_CONFIG=$(CDPATH= cd -- "$(dirname -- "$SOURCE_CONFIG")" && pwd)/$(basename -- "$SOURCE_CONFIG")

# Keep the portable Git behavior in AgentDesk and let ~/.gitconfig retain
# machine/user-specific identity and credentials.
git config --global --replace-all include.path "$SOURCE_CONFIG" '^.*/AgentDesk/config/git/gitconfig$' 2>/dev/null ||
  git config --global --add include.path "$SOURCE_CONFIG"

echo "Installed AgentDesk Git config: $SOURCE_CONFIG"
echo "Available: git review <commit>, git review-range [<base> [<target>]], git unreview"
