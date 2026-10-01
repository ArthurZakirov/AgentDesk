# ⌨️ Cross-Mac shortcuts

## Desired behavior

These are the user's selected defaults. Apply them on each Mac using that machine's paths; do not synchronize the contents of the target files.

| Entry point | Behavior | Machine-specific input |
| --- | --- | --- |
| Raycast `zsh` + Return | Open the active Zsh configuration in VS Code | Zsh configuration location; usually `~/.zshrc`, but check `ZDOTDIR` |
| Raycast `agent` + Return | Open global Codex guidance in VS Code | Codex home; normally `~/.codex/AGENTS.md`, but honor `CODEX_HOME` |
| Raycast `desk` + Return | Open the normal AgentDesk checkout's README in VS Code | Absolute location of the normal checkout; never substitute a worktree |
| Option-Q | Show all windows of the current application (App Exposé) | Native macOS “Application windows” shortcut |

Use the same aliases on both Macs. The repository location and configuration contents can differ. The work Mac's paths and setup have not been inspected.

## 🔄 Source and synchronization

AgentDesk owns this reproducible setup recipe. The parent [productivity skill](../SKILL.md) is its agent entry point; humans can use this page directly. A one-time configuration needs a maintained recipe and verification, not a continuously running agent or a separate installed skill.

Raycast's [Cloud Sync](https://manual.raycast.com/cloud-sync) requires a signed-in Pro account. It supports Quicklinks and selected settings. It does not synchronize native macOS shortcuts, and Script Command files must be distributed separately even though their settings sync. Check the current manual before enabling categories; account synchronization does not translate machine-specific paths.

For these three local file targets, start with this recipe and a locally generated Quicklinks import. Cloud Sync is optional. If syncing Quicklinks, prefer home-relative links when locations match. For an AgentDesk checkout at different locations, either establish the same home-relative local alias path on both Macs or use a shared Script Command with a local path configuration. Do not keep editing one cloud-synced absolute path differently on each machine.

Keep complete Raycast exports, account data, work repository names, and work-machine inventories outside this public repository. Commit portable recipes and generic templates only. Use an account/cloud setup on the work Mac only where the employer permits it.

## 📂 Raycast setup

1. Inspect target locations without reading configuration contents. Check whether VS Code and Raycast are installed. Check whether the destination alias already exists; update that entry rather than creating a competing alias.
2. Determine the normal AgentDesk checkout path on this machine. Generate the import below with that path. Home and environment overrides are resolved locally.
3. In Raycast, run **Import Quicklinks** and select the generated JSON. This adds entries rather than replacing all settings. A changed path may create a second entry; reconcile an existing named entry through **Search Quicklinks → Edit Quicklink** instead.
4. In **Settings → Quicklinks**, set `zsh`, `agent`, and `desk` on their respective entries. The documented JSON import fields do not include aliases; set them through the supported UI. Select VS Code in **Open With** if it did not resolve during import.
5. Open the normal AgentDesk folder in VS Code once, select its README, and show **Explorer** with Shift-Command-E. The Quicklink opens the README; it does not force the folder to become the workspace or force Explorer visible on every invocation. VS Code normally remembers the workspace layout. Verify the target even when multiple windows are open.

Generate the JSON in a temporary location, replacing the example checkout argument:

```bash
python3 - "$HOME/Repos/personal/AgentDesk" <<'PY'
import json
import os
import sys
import tempfile
from pathlib import Path

home = Path.home()
repo = Path(sys.argv[1]).expanduser().resolve()
zsh = Path(os.environ.get('ZDOTDIR') or home).expanduser() / '.zshrc'
codex = Path(os.environ.get('CODEX_HOME') or home / '.codex').expanduser() / 'AGENTS.md'
targets = [('Zsh Config', zsh), ('Codex Agents MD', codex), ('AgentDesk Repo', repo / 'README.md')]
missing = [str(path) for _, path in targets if not path.is_file()]
if missing:
    raise SystemExit('Resolve these missing targets before importing: ' + ', '.join(missing))
with tempfile.NamedTemporaryFile(mode='w', prefix='raycast-editor-', suffix='.json', delete=False) as out:
    json.dump([{'name': name, 'link': str(path), 'openWith': 'Visual Studio Code'}
               for name, path in targets], out, indent=2)
    out.write('\n')
    print(out.name)
PY
```

Source: [Raycast Quicklinks import format](https://manual.raycast.com/quicklinks) and [aliases](https://manual.raycast.com/command-aliases-and-hotkeys).

## 🪟 Native App Exposé setup

Use **System Settings → Keyboard → Keyboard Shortcuts → Mission Control → Application windows**. Replace Control-Down with Option-Q. This changes the native binding; it does not require Raycast or Hammerspoon to run.

On the private Mac, the native setting was applied and the user confirmed Option-Q worked on 2026-10-01. Reverify on another macOS version or keyboard layout; this observation is not proof for the work Mac.

For a script-based setup on a compatible Mac, back up preferences first and change only symbolic hotkey 33. This is a macOS implementation detail, not a stable public API; fall back to the settings UI if verification fails. XML preserves actual boolean/integer types rather than string values.

```bash
shortcut_backup="$(mktemp -t app-expose-backup).plist"
defaults export com.apple.symbolichotkeys "$shortcut_backup"
printf 'Backup: %s\n' "$shortcut_backup"
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 33 \
  '<dict><key>enabled</key><true/><key>value</key><dict><key>parameters</key><array><integer>113</integer><integer>12</integer><integer>524288</integer></array><key>type</key><string>standard</string></dict></dict>'
activation_tool='/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings'
if [ -x "$activation_tool" ]; then "$activation_tool" -u; fi
```

Inspect only the relevant preference:

```bash
python3 - <<'PY'
import plistlib
import subprocess
data = plistlib.loads(subprocess.check_output(['defaults', 'export', 'com.apple.symbolichotkeys', '-']))
print(data.get('AppleSymbolicHotKeys', {}).get('33', 'System default; no explicit override'))
PY
```

The selected configuration should report `enabled: True`, `type: standard`, and parameters `[113, 12, 524288]`. Quit/reopen System Settings before inspecting its display if it was open during a scripted change. To undo, edit only **Application windows** back to Control-Down in the UI; do not restore an entire old preference export over unrelated later changes.

## ✅ Handoff verification

1. Search each exact Raycast alias and verify its first result. Invoke it and inspect the absolute target, not just the VS Code window title.
2. For `desk`, verify the normal AgentDesk folder is the workspace, README is selected, and Explorer displays that folder. A restored tab from another folder can coexist inside the correct workspace.
3. With two windows of one application open, press Option-Q and confirm the overview contains those windows. Dismiss it with Escape.
4. Record which machine was tested and any unverified result. Do not claim cross-device synchronization is enabled merely because one Mac was configured.

## 💬 Prompt for another Mac

> Use AgentDesk's setup-macbook-productivity skill and its Cross-Mac shortcuts reference. Configure the same Raycast aliases zsh, agent, and desk for this Mac's local Zsh configuration, global Codex AGENTS.md, and normal AgentDesk checkout README, all opening in VS Code. Determine paths locally and preserve existing entries. Set native App Exposé to Option-Q. Use supported configuration/import mechanisms first and Computer Use for alias assignment or settings that lack a supported file interface. Verify the actual targets and the window overview; report any blocker. Do not enable cloud synchronization or transfer work data as part of this local setup.
