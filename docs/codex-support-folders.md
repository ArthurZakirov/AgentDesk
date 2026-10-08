# 🗂️ Codex support folders

Codex runtime files stay at the Codex home root. Keep configuration inputs in `config-toml/` and hook support in `hooks-json/`, with one subfolder per hook.

## ⚙️ Configuration renderer

The canonical [renderer](../scripts/render-codex-config.py) defaults to the template and realtime prompt under `~/.codex/config-toml/`, and writes `~/.codex/config.toml`. Explicit `--template`, `--prompt`, and `--output` arguments remain available.

Deploy the renderer after reviewing changes:

```bash
mkdir -p "$HOME/.codex/config-toml"
cp scripts/render-codex-config.py "$HOME/.codex/config-toml/render-config.py"
```

Keep personal template and prompt contents local. To regenerate configuration intentionally:

```bash
python3 "$HOME/.codex/config-toml/render-config.py"
```

Regeneration replaces the runtime configuration with the template output; review local configuration drift before running it.

## 🪝 Hook support

The [bedtime installer](../skills/bedtime-device-guard/scripts/install_guard.py) installs under `hooks-json/bedtime-device-guard/` and keeps registration in root `hooks.json`. Reinstallation migrates an existing legacy support directory when the new destination does not exist. See the [guard skill](../skills/bedtime-device-guard/SKILL.md) for installation and verification.

Restart Codex sessions after moving hook support and review/trust the changed command in `/hooks` when prompted. Keep any existing schedule during a path-only migration. Back up hook registration before atomically updating paths, preserving unrelated handlers.

To inspect the local support layout without reading configuration contents:

```bash
find "$HOME/.codex/config-toml" "$HOME/.codex/hooks-json" -maxdepth 2 -type f
```
