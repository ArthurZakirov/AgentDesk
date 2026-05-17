# AgentDesk

Make any machine ready for human and AI-agent work.

AgentDesk packages repeatable setup skills for the local workstation layer: WSL2, macOS, browsers, monitors, Codex, Claude Code, OpenClaw, Bitwarden-backed personal profiles, and the small repair workflows that make agents useful on a real machine.

The repo exists so a fresh or broken workstation can be brought back to a productive, agent-ready state without reconstructing setup knowledge from memory.

## What It Helps With

- Configure macOS window management, dictation, monitors, and daily-driver productivity settings.
- Set up WSL2 browser bridges and agent-browser runtimes.
- Repair OpenClaw and browser-control workflows.
- Keep personal form-fill profile data outside Git while making it usable by agents.
- Install the same workstation skills across Codex and Claude Code.

## Install With skills.sh

List the skills in this repo:

```bash
npx skills add https://github.com/ArthurZakirov/AgentDesk --list
```

Install all skills for Codex on a machine:

```bash
npx skills add https://github.com/ArthurZakirov/AgentDesk --skill '*' -a codex -g -y
```

Install one specific skill:

```bash
npx skills add https://github.com/ArthurZakirov/AgentDesk --skill wsl2-browser-setup -a codex -g -y
```

## Install As A Claude Code Plugin

```text
/plugin marketplace add ArthurZakirov/AgentDesk
/plugin install agentdesk@arthur-zakirov
```

Claude Code plugin skills are namespaced by plugin name, for example:

```text
/agentdesk:wsl2-browser-setup
```

## Install As A Codex Plugin

This repo includes Codex plugin packaging:

- repo marketplace metadata at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- plugin manifest at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json)

Add the marketplace:

```bash
codex plugin marketplace add ArthurZakirov/AgentDesk
```

Then install from Codex with `/plugins`.

For local development from a cloned repo:

```bash
./scripts/setup-local-links.sh
```

Existing non-symlink paths are left untouched unless `--force` is used.

## Included Skills

<!-- BEGIN GENERATED SECTION: skills -->
> Generated from tracked `skills/*/SKILL.md` metadata.

| Skill | Description |
| --- | --- |
| `aerospace-macos-setup` | Install, configure, and debug AeroSpace on macOS. Use when Codex needs to set up AeroSpace with Homebrew, create or repair ~/.aerospace.toml, configure window movement hotkeys for multi-monitor workflows, diagnose Accessibility or server/config problems, or automate binding tests with the AeroSpace CLI. |
| `agent-browser-wsl2-setup` | Install and configure `agent-browser` on a Windows machine with WSL2 after a browser path is already working. Use when a user wants the `agent-browser` CLI, its downloaded runtime, the `vercel-labs/agent-browser` repository, or an `agent-browser` attachment to a Windows host browser bridge from WSL2. |
| `bitwarden-personal-profile` | Load, validate, and use a user's private personal profile from Bitwarden CLI for form filling, PDF completion, applications, and identity/contact/employment/housing reuse. Use when an agent needs stable personal data backed by Bitwarden, language-aware profile values, a bundled schema for personal facts, or a safe workflow that materializes real profile values outside Git. |
| `openclaw-browser-setup` | Troubleshoot and operate OpenClaw browser on local or remote gateways. Use when Codex needs to enable the bundled browser plugin, resolve `pairing required` or device approval errors, choose between the managed `openclaw` profile and the attached `user` profile, handle Linux headless or Chrome CDP startup failures, or prove browser control with `profiles`, `start`, `open`, `snapshot`, and `screenshot`. |
| `setup-dell-monitors` | Troubleshoot Arthur's Dell P2725DE/P2225D monitor setup, especially DisplayPort daisy chaining, "No DP signal from your device" on the P2225D, Windows Fast Startup or shutdown-related display breakage, and reset/reinstall steps for a Lenovo laptop or Dell desktop tower using original Dell cables. |
| `setup-macbook-productivity` | Configure repeatable macOS productivity settings on a user's MacBook, especially voice typing / Dictation setup. Use when Codex is asked to set up, repair, or document MacBook productivity features such as voice typing, Dictation, Dictation shortcuts, microphone input for Dictation, or future local macOS workflow preferences. |
| `wsl2-browser-setup` | Install and configure browsers for Windows plus WSL2. Use when a user wants native Linux Chrome inside WSL to work for normal browsing or sign-in flows, or when a tool in WSL needs a Windows host Chrome or Edge instance exposed over CDP. Prefer this skill before any tool-specific browser automation setup. |
<!-- END GENERATED SECTION: skills -->

## Available Commands

<!-- BEGIN GENERATED SECTION: commands -->
> Generated from tracked `commands/*.md` files.

| Command | Summary |
| --- | --- |
| `/list-skills` | Please list all your available skills with a 1 sentence description for each one. Do not return any additional fluff text before or after. |
<!-- END GENERATED SECTION: commands -->

## Repo Inventory

<!-- BEGIN GENERATED SECTION: repo_inventory -->
> Generated from tracked manifests, scripts, commands, and skills.

```text
.
├── .agents/
│   ├── plugins/marketplace.json
│   └── skills -> ../skills
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .claude/
│   ├── commands -> ../commands
│   └── skills -> ../skills
├── .codex-plugin/
│   └── plugin.json
├── .githooks/
│   └── pre-commit
├── .github/
│   └── workflows/
│       └── readme-generated.yml
├── commands/
│   └── list-skills.md
├── scripts/
│   ├── create-claude-command.sh
│   ├── create-shared-skill.sh
│   ├── generate-readme.py
│   ├── install-git-hooks.sh
│   ├── setup-local-links.sh
│   └── update-readme.sh
├── skills/
│   ├── aerospace-macos-setup/
│   ├── agent-browser-wsl2-setup/
│   ├── bitwarden-personal-profile/
│   ├── openclaw-browser-setup/
│   ├── setup-dell-monitors/
│   ├── setup-macbook-productivity/
│   └── wsl2-browser-setup/
├── pyproject.toml
└── uv.lock
```
<!-- END GENERATED SECTION: repo_inventory -->

## Development

Use `./scripts/update-readme.sh` after adding or removing tracked skills, commands, scripts, or plugin metadata.
