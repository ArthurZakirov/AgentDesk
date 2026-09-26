<a id="git-workflow"></a>
# 🔀 Git workflow

## Local file changes

**When**

- Creating, editing, moving, renaming, or deleting files on the local computer.

**Then**

- Determine whether the affected path belongs to a Git repository.
- If it is in a Git repository, apply the repository workflow below.
- If it is not in a Git repository, do not invent Git steps; preserve unrelated local files and validate the changed artifact using the tooling appropriate to that file or system.

## Repository workflow

**When**

- Working in a Git repository and making or preparing changes.

**Then**

- Inspect the repository's actual hook, validation, and workflow configuration before assuming a standard process.
- Enable or use the repository's documented hooks when provided.
- Preserve unrelated local work; do not discard, overwrite, or silently absorb unrelated changes.

## Before an authorized push

**When**

- A push is explicitly authorized.

**Then**

- Inspect staged changes and repository divergence first.
- Run the applicable local pre-commit, pre-push, and validation checks.
- Treat passing checks as validation only; they do not authorize additional commits, edits, or pushes.

## After a push

**When**

- A push has completed and corresponding remote checks are available.

**Then**

- Monitor those checks through completion.
- If a check fails, read the failure evidence, fix only within the authorized scope, validate again, and monitor again.
- Report external or out-of-scope blockers clearly; an empty check list is not itself a failure.
