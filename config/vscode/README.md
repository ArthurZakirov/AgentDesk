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

The tasks run from the workspace folder and do not require an open editor.
`Git: Unreview` also finds a review launched from the source checkout. If several
reviews exist for that checkout, run `git unreview` inside the review you want to
close; the helper refuses to choose one arbitrarily.

Use `⇧⌘P` → `Tasks: Run Task`, then choose the Git task. The source checkout
stays untouched while VS Code displays ordinary working-tree changes in the
temporary review checkout, preserving editor navigation such as go-to-definition.

A task label is not itself a top-level Command Palette command; registering
`Git: Review Range` directly at the palette root would require a VS Code extension.
