# Git configuration

This directory contains portable Git behavior shared across workstations.

Keep machine- or identity-specific values such as `user.name`, `user.email`,
credential helpers, signing keys, and filesystem paths out of this file.

Install the shared config with:

```sh
./scripts/install-git-config.sh
```

The installer adds this tracked file through Git's global `include.path`, so the
normal per-machine `~/.gitconfig` remains available for local settings.

## Review aliases

- `git review <commit>`: materialize one commit as editable working-tree changes.
- `git review-range`: materialize HEAD versus the fetched upstream remote's default branch.
- `git review-range <base> [<target>]`: materialize an explicit range using its merge base.
- `git unreview`: discard the temporary materialization and return to the original branch/revision.

`review-range` requires a clean working tree before entering review mode and does
not rewrite, squash, reset, or otherwise modify the reviewed branch's commits.
