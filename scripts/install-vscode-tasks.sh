#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE="$SCRIPT_DIR/../config/vscode/tasks.json"

case "$(uname -s)" in
  Darwin) TARGET="$HOME/Library/Application Support/Code/User/tasks.json" ;;
  Linux) TARGET="${XDG_CONFIG_HOME:-$HOME/.config}/Code/User/tasks.json" ;;
  *)
    echo "Automatic VS Code user-task installation is not configured for this OS." >&2
    echo "Copy $SOURCE to your VS Code User/tasks.json location." >&2
    exit 1
    ;;
esac

mkdir -p "$(dirname -- "$TARGET")"
if [ -e "$TARGET" ] && ! cmp -s "$SOURCE" "$TARGET"; then
  echo "Refusing to overwrite existing VS Code user tasks: $TARGET" >&2
  exit 1
fi

cp "$SOURCE" "$TARGET"
echo "Installed VS Code user tasks: $TARGET"
echo "Run Command Palette > Tasks: Run Task > Git: Review Range / Git: Unreview"
