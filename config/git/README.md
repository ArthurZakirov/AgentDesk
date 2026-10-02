# Git configuration

This directory contains portable Git behavior shared across workstations.

Keep machine- or identity-specific values such as `user.name`, `user.email`,
credential helpers, signing keys, and filesystem paths out of this file.

Install with:

```sh
./scripts/install-git-config.sh
```

The installer copies the portable config to `~/.config/agentdesk/gitconfig`,
installs the review helper as `~/.local/bin/agentdesk-git-review`, and includes
the config from the normal per-machine `~/.gitconfig`.

## Isolated review worktrees

Review commands never rewrite or dirty the source worktree. They create a
disposable detached worktree under `~/.local/share/agentdesk/reviews/`,
materialize the requested diff there, record the source worktree in Git metadata,
and open the review worktree in VS Code when the `code` CLI is available.

- `git review <commit>`: review one commit against its parent.
- `git review-range`: review HEAD against the fetched upstream remote's default branch.
- `git review-range <base> [<target>]`: review an explicit range using its merge base.
- `git unreview`: from a review worktree, reopen the source worktree and remove the disposable review.

The source branch and its individual commits remain unchanged throughout review.
The metadata file `AGENTDESK_REVIEW.json` lives in the review worktree's Git
metadata rather than its working tree, so it cannot appear as a review change.
