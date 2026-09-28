# AgentDesk development guidance

AgentDesk is the canonical source for Arthur's workstation skills and global agent guidance. Treat repository sources as editable; generated machine-local outputs are deployment artifacts.

## Repository model

| When | Then |
| --- | --- |
| Changing global agent guidance. | Edit files under `global-guidance/agents-md-components/`, `global-guidance/agents-md-references/`, and/or `global-guidance/agents-md-manifest.yaml`. Do not edit the generated global `~/AGENTS.md`, `~/.claude/CLAUDE.md`, or OpenCode output as the source of truth. |
| Adding, removing, reordering, or grouping global guidance components. | Update `global-guidance/agents-md-manifest.yaml`. The manifest is the semantic source of truth for order and parent/child hierarchy; component folders alone do not imply nesting. Parent components may declare `children`, which render beneath the parent while remaining separate source files. |
| Changing a workstation skill. | Edit the repository `skills/` source. Treat globally installed `npx skills` copies as generated deployments. |
| Editing parked desired behavior. | Use `global-guidance/wishlist/`; wishlist content is intentionally not active production guidance until promoted through the behavior lifecycle. |
## Generated guidance and tests

| When | Then |
| --- | --- |
| Global guidance sources change. | Regenerate the rendered guidance with `python3 scripts/regenerate-agents-md.py` using explicit test/temporary harness homes when validating, or the real configured homes when intentionally deploying. |
| `tests/test_agents_md_preview.py` fails after an intentional guidance change. | Treat the failure as a stale generated preview until proven otherwise. Regenerate `tests/fixtures/agents-md-preview/macos/` from the same manifest/generator, inspect the diff, and commit the fixture only if it faithfully represents the intended output. Do not weaken or bypass the snapshot test. |
| A relative-link preview test fails. | Fix the canonical component/reference link or generator behavior. Do not patch only the fixture. |
| Generator behavior changes. | Run both bootstrap/regeneration tests and preview tests; verify preservation, hierarchical ordering, heading demotion, global and local nested TOC rendering, harness imports, idempotency, and generated-reference behavior remain correct. |

The preview fixture is a checked-in expected rendering of the global guidance, not an independent source of truth.
## Validation and commit flow

| When | Then |
| --- | --- |
| Before treating an AgentDesk change as complete. | Run `uv run pytest -q` and `git diff --check`. Run `./scripts/update-readme.sh` when tracked skills, commands, scripts, plugin metadata, or repo inventory changed. |
| The pre-commit hook runs. | Expect it to regenerate `README.md` and stage it. Inspect any README diff as generated output caused by the source change; do not hand-edit generated sections. |
| Tests reveal an unexpected generated diff. | Diagnose which canonical source or generator produced it before changing tests or fixtures. |
| Preparing a commit/push. | Inspect `git status`, staged diff, branch, and divergence. Include only coherent AgentDesk changes and their required generated artifacts. |

## Architecture references

- `scripts/bootstrap-agents-md.py` implements manifest loading, rendering, installation, preservation, and runtime-reference sync.
- `scripts/install-global-guidance.sh` is the clone-independent remote installer for the checked-in generated Codex guidance preview, runtime references, and a local mirror of the canonical guidance sources used by its Markdown links.
- `scripts/regenerate-agents-md.py` is the thin entrypoint for rebuilding global guidance from the manifest.
- `tests/test-bootstrap-agents-md.py` protects preservation, manifest ordering, imports, idempotency, and reference sync.
- `tests/test-regenerate-agents-md.py` protects the regeneration entrypoint contract.
- `tests/test_agents_md_preview.py` protects the checked-in rendered preview and relative-link integrity.
