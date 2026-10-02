#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_CONFIG="$SCRIPT_DIR/../config/git/gitconfig"
INSTALL_DIR="$HOME/.config/agentdesk"
INSTALLED_CONFIG="$INSTALL_DIR/gitconfig"

if [ ! -f "$SOURCE_CONFIG" ]; then
  echo "Missing $SOURCE_CONFIG" >&2
  exit 1
fi

mkdir -p "$INSTALL_DIR"
cp "$SOURCE_CONFIG" "$INSTALLED_CONFIG"

# Keep portable behavior at a stable per-user path. ~/.gitconfig remains the
# machine/user-specific layer for identity, credentials, signing, and paths.
git config --global --unset-all include.path '.*AgentDesk/config/git/gitconfig$' 2>/dev/null || true
git config --global --replace-all include.path "$INSTALLED_CONFIG" '^.*/\.config/agentdesk/gitconfig$' 2>/dev/null ||
  git config --global --add include.path "$INSTALLED_CONFIG"

echo "Installed AgentDesk Git config: $INSTALLED_CONFIG"
echo "Available: git review <commit>, git review-range [<base> [<target>]], git unreview"
