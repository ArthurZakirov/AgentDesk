# Troubleshooting

## Native Chrome Opens But External Sites Fail

1. Ensure Windows `.wslconfig` contains:

   ```ini
   [wsl2]
   networkingMode=mirrored
   dnsTunneling=true
   ```

2. Run `wsl --shutdown`.
3. Reopen WSL.
4. Open `chrome://settings/security`.
5. Turn `Use secure DNS` fully off. `OS default (when available)` means it is still enabled.

## A Site Works But The Sign-In Flow Fails In Headless Tests

Use the interactive browser as the browser-layer ground truth. If the target site and sign-in page render in interactive Chrome, investigate the automation client instead of repeating browser setup.

## Chrome Prints Noisy Errors

These messages were harmless in the proven setup:

- `dbus ... UPower ... ServiceUnknown`
- `Created TensorFlow Lite XNNPACK delegate for CPU`
- `Registration response error message: DEPRECATED_ENDPOINT`
- `Registration URL fetching failed`

Judge success by page loading and sign-in behavior, not console noise alone.

## Windows Host Bridge Is Unreachable

Check, in order:

1. The Windows browser is running with the requested remote-debugging port.
2. The Windows elevation step completed.
3. `http://HOST_IP:BRIDGE_PORT/json/version` responds from WSL2.

Rerun the bridge helper before making lower-level firewall or networking changes:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh" --check-only
```

## `agent-browser` Is Missing

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-agent-browser-runtime.sh"
```

## Native `agent-browser` Hangs After Manual Chrome Works

Treat this as a client-layer failure. Check `agent-browser doctor --offline --quick`, then use the Windows bridge path if native control still hangs.

## `connect-windows-browser.sh` Fails

First prove that the bridge responds on `/json/version` with the bridge helper's `--check-only` mode. Repair the bridge if that endpoint is unavailable; otherwise inspect the `agent-browser` client.

## The Upstream Skill Installer Blocks Progress

`npx skills add vercel-labs/agent-browser` is interactive and belongs to the human. It is optional unless the user specifically wants that upstream skill package; the CLI and runtime installer can proceed independently.
