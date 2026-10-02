#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_CONFIG="$SCRIPT_DIR/../config/git/gitconfig"
SOURCE_REVIEW="$SCRIPT_DIR/git-review-worktree.py"
CONFIG_DIR="$HOME/.config/agentdesk"
BIN_DIR="$HOME/.local/bin"
INSTALLED_CONFIG="$CONFIG_DIR/gitconfig"
INSTALLED_REVIEW="$BIN_DIR/agentdesk-git-review"

mkdir -p "$CONFIG_DIR" "$BIN_DIR"
cp "$SOURCE_CONFIG" "$INSTALLED_CONFIG"
cp "$SOURCE_REVIEW" "$INSTALLED_REVIEW"
chmod +x "$INSTALLED_REVIEW"

git config --global --unset-all include.path '.*AgentDesk/config/git/gitconfig$' 2>/dev/null || true
git config --global --replace-all include.path "$INSTALLED_CONFIG" '^.*/\.config/agentdesk/gitconfig$' 2>/dev/null ||
  git config --global --add include.path "$INSTALLED_CONFIG"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "Warning: add $BIN_DIR to PATH so Git review aliases can find agentdesk-git-review." >&2 ;;
esac

echo "Installed AgentDesk Git config: $INSTALLED_CONFIG"
echo "Installed review helper: $INSTALLED_REVIEW"
