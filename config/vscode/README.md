# VS Code user configuration

This directory contains portable VS Code user-level configuration that should be
available across repositories rather than checked into each project.

## User tasks

`tasks.json` defines:

- `Git: Review Range` — runs `git review-range` in the active workspace.
- `Git: Unreview` — runs `git unreview` in the active workspace.

Install with:

```sh
./scripts/install-vscode-tasks.sh
```

In VS Code use `⇧⌘P` → `Tasks: Run Task`, then choose the Git task.

VS Code user tasks are the native configuration mechanism for cross-workspace
shell/process tasks. A task label is not itself registered as a top-level Command
Palette command; that would require a VS Code extension.
