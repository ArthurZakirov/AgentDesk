<a id="git-workflow"></a>
# 🔀 Git workflow for all GitHub repositories

- Follow each repository's actual hook and validation tooling. If it provides hooks or configuration, install or enable them using its documented setup; do not assume every repository uses the same framework.
- Before each authorized push, run applicable local pre-commit, pre-push, and validation checks. Review staged changes and preserve unrelated work; hook setup or a passing check does not authorize additional commits or pushes.
- After pushing, monitor corresponding checks through completion when available. Read failed logs and fix failures within the authorized scope, then validate and monitor again. Report external or out-of-scope blockers clearly; an empty check list is not itself a failure.
