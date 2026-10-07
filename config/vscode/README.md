# VS Code user configuration

This directory contains portable VS Code user-level configuration shared across
repositories.

## Git review tasks

`tasks.json` defines:

- `Git: Review Range` — opens the current branch diff in an isolated review worktree.
- `Git: Review Last Commit` — opens HEAD against its parent in an isolated review worktree.
- `Git: Review Specific Commit` — prompts for a hash, tag, or revision and opens that commit.
- `Git: Unreview` — returns to the recorded source worktree and removes the review worktree.

Install with:

```sh
./scripts/install-vscode-tasks.sh
```

The tasks run in the directory of the active editor file. Select a file in the
repository you want to review; for `Git: Unreview`, select a file in the temporary
review checkout. This also works when the window contains several repositories.

Use `⇧⌘P` → `Tasks: Run Task`, then choose the Git task. The source checkout
stays untouched while VS Code displays ordinary working-tree changes in the
temporary review checkout, preserving editor navigation such as go-to-definition.

A task label is not itself a top-level Command Palette command; registering
`Git: Review Range` directly at the palette root would require a VS Code extension.
