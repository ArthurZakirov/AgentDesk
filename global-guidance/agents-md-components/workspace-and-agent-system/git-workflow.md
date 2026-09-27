<a id="git-workflow"></a>
# 🔀 Git workflow

| When | Then |
| --- | --- |
| Creating, editing, moving, renaming, or deleting files on the local computer. | Determine whether the affected path belongs to a Git repository. If yes, apply the repository workflow below. If no, do not invent Git steps; preserve unrelated local files and validate with tooling appropriate to that artifact/system. |
| Working in a Git repository and making or preparing changes. | Inspect the repository's actual hook, validation, and workflow configuration; use documented hooks when provided; preserve unrelated local work. |
| A coherent set of repository changes is ready. | Inspect staged changes and divergence; run applicable pre-commit, pre-push, and validation checks; commit the intended changes and push them by default without asking for separate authorization. Do not push only when a check fails, divergence/conflict makes the safe action unclear, credentials or remote access block the push, or repository-specific instructions explicitly require a different workflow. |
| A push completed and corresponding remote checks are available. | Monitor checks through completion. For failures, inspect evidence, fix only within authorized scope, validate, and monitor again. Report external/out-of-scope blockers; an empty check list is not itself a failure. |
