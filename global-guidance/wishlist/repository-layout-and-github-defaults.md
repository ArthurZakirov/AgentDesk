# Repository layout and GitHub defaults

Migrated from the former machine-global `/Users/zakirov/AGENTS.md`; parked here until the desired behavior and proper canonical location are validated.

## Repository layout

- Use `$PERSONAL_REPOS_DIR` for repositories owned by ArthurZakirov or created for Arthur's own projects.
- Use `$OPEN_SOURCE_REPOS_DIR` for third-party open source repositories cloned for reading, patching, testing, or contribution work.
- Use `$REPOS_DIR` as the parent directory for local repository organization.
- Do not hardcode these repository paths in commands, docs, or instructions when the environment variables can be used instead.
- Do not clone repositories directly into `$HOME`, `~/Desktop`, `~/Documents`, or `~/Downloads` unless explicitly requested.
- Before cloning a repository, choose the destination based on ownership:
  - Personal GitHub repositories: `$PERSONAL_REPOS_DIR/<repo-name>`
  - Other people's or organization-owned open source repositories: `$OPEN_SOURCE_REPOS_DIR/<repo-name>`

## GitHub defaults

- Personal GitHub account: `ArthurZakirov`.
- Prefer SSH remotes for GitHub repositories.
- Keep personal work and external open source work separated by the environment-variable folders above.
