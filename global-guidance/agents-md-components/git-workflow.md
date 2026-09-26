<a id="git-workflow"></a>
# 🔀 Git workflow

| When | Then |
| --- | --- |
| Creating, editing, moving, renaming, or deleting files on the local computer. | Determine whether the affected path belongs to a Git repository. If yes, apply the repository workflow below. If no, do not invent Git steps; preserve unrelated local files and validate with tooling appropriate to that artifact/system. |
| Working in a Git repository and making or preparing changes. | Inspect the repository's actual hook, validation, and workflow configuration; use documented hooks when provided; preserve unrelated local work. |
| A push is explicitly authorized. | Inspect staged changes and divergence first; run applicable pre-commit, pre-push, and validation checks; treat passing checks as validation, not authorization for additional work. |
| A push completed and corresponding remote checks are available. | Monitor checks through completion. For failures, inspect evidence, fix only within authorized scope, validate, and monitor again. Report external/out-of-scope blockers; an empty check list is not itself a failure. |
