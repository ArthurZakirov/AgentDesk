# 🧪 Chezmoi global-guidance pilot

This pilot tests chezmoi as a reversible **device apply layer** for AgentDesk's generated Codex guidance. AgentDesk remains the only editable source: the pilot renders [`global-guidance/`](../global-guidance/) into an ephemeral chezmoi source tree, and chezmoi copies only `AGENTS.md` and `agents-md-references/` into the selected Codex home.

It does not manage skills, refresh Git checkouts, schedule updates, configure Claude Code or OpenCode, or write chezmoi configuration into the user's home.

## Safety contract

| Concern | Pilot behavior |
| --- | --- |
| First run | `plan` is dry-run only. `apply` also runs the same dry-run before any write. An unmanaged existing guidance file blocks apply unless `--replace-existing` is explicit. |
| Existing files | Every existing managed target is copied to a timestamped machine-local backup before chezmoi runs. |
| Conflicts | Chezmoi runs non-interactively with `--error-on-conflict=true`; it does not silently answer an overwrite prompt. |
| Rollback | `rollback` restores the latest pre-apply backup and removes only pilot-managed files that did not exist in that backup. Do not use `chezmoi destroy`, which chezmoi documents as permanently removing source and destination files. |
| Paths | The Codex home must be one direct child of the selected home. This covers the default `.codex` location under macOS/Linux `$HOME` and Windows `%USERPROFILE%` without committing either machine's absolute path. |
| Secrets | The ephemeral source contains generated AgentDesk guidance only. Put machine-local paths or secret-provider configuration in local, permission-restricted configuration—not in this repository or the generated payload. |
| Scope | The pilot never targets the live home during tests. A live apply requires a human to run the explicit command after inspecting the plan. |

## Run the pilot

Prerequisite: install `chezmoi` through the platform's trusted package manager and confirm it with `chezmoi doctor`.

Preview the exact changes:

```bash
uv run python scripts/chezmoi-guidance-pilot.py plan
```

If the preview would replace reconciled existing guidance, apply explicitly:

```bash
uv run python scripts/chezmoi-guidance-pilot.py apply --replace-existing
```

Restore the latest pre-apply state:

```bash
uv run python scripts/chezmoi-guidance-pilot.py rollback
```

For a temporary test home, keep all state outside the real home:

```bash
pilot_home="$(mktemp -d)"
uv run python scripts/chezmoi-guidance-pilot.py plan --home "$pilot_home" --state-dir "$pilot_home/state"
```

On native Windows PowerShell, pass native paths rather than relying on shell-home translation:

```powershell
uv run python scripts/chezmoi-guidance-pilot.py plan `
  --home $env:USERPROFILE `
  --codex-home (Join-Path $env:USERPROFILE '.codex')
```

The machine-local default backup location is derived at runtime. Inspect it with the command output after `apply`; do not copy a concrete device path into shared documentation.

## Why this is not a SkillPort replacement

| Responsibility | AgentDesk + chezmoi pilot | SkillPort |
| --- | --- | --- |
| Canonical guidance composition | AgentDesk manifest, components, references, and generator | Invokes AgentDesk; must not duplicate its generator |
| Codex guidance apply | Chezmoi, limited to generated Codex files | Existing refresh scripts currently intend to invoke AgentDesk directly |
| Repository refresh | Out of scope | Registry-scoped safe Git refresh |
| Skills | Out of scope | Explicit registry/manifest-driven `npx skills` install/update |
| Scheduling | Out of scope | macOS LaunchAgent and Windows Task Scheduler |
| Rollback | Timestamped pilot backup plus explicit rollback | Generator backup on first reconciled replacement |

Chezmoi is useful here only if its preview, cross-platform destination model, and rollback boundary are preferred over the generator's direct file writes. SkillPort remains the broader fleet-refresh orchestrator. A production rollout should choose one owner for the final guidance apply step so SkillPort and chezmoi never race over the same files.

## Observed SkillPort interface mismatch

Reproduce against sibling checkouts with:

```bash
rg -n -- '--common|--overlay|--platform|global-guidance/(common|macos|windows-wsl)\.md' \
  ../SkillPort/scripts
python3 scripts/bootstrap-agents-md.py --help
```

At the time of this pilot, SkillPort's macOS and Windows refresh scripts call the removed `--common`, `--overlay`, and `--platform` interface and reference removed flat guidance files. AgentDesk now requires `--manifest` (normally through [`regenerate-agents-md.py`](../scripts/regenerate-agents-md.py)) and accepts explicit harness-home targets. This prevents the documented SkillPort global-guidance refresh from succeeding until SkillPort is updated. The mismatch is outside this repository's implementation scope and should be fixed in SkillPort before any live unattended rollout.

## Verification

Run the repository checks:

```bash
uv run pytest -q
git diff --check
```

The pilot tests render into temporary homes, verify target-relative links, prove an unmanaged first run fails closed, and prove apply/rollback restores the prior state. These tests use a fake chezmoi executable to avoid touching live configuration. Before production adoption, run the same plan/apply/rollback sequence with a real chezmoi binary in temporary homes on both macOS and native Windows.

## Official chezmoi references

- [Concepts: source, destination, target, and machine-local config](https://www.chezmoi.io/reference/concepts/)
- [Global flags: source, destination, dry-run, and conflict handling](https://www.chezmoi.io/reference/command-line-flags/global/)
- [`apply` and its dry-run example](https://www.chezmoi.io/reference/commands/apply/)
- [`diff` for inspecting target versus destination](https://www.chezmoi.io/reference/commands/diff/)
- [Machine-to-machine templates and local data](https://www.chezmoi.io/user-guide/manage-machine-to-machine-differences/)
- [`destroy` warning](https://www.chezmoi.io/reference/commands/destroy/)
