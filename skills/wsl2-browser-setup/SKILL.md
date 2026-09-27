---
name: wsl2-browser-setup
description: Set up browser access from WSL2 through native Linux Chrome or a Windows Chrome/Edge CDP bridge, with optional `agent-browser` installation and attachment. Use for WSL2 browsing, sign-in, connectivity, or browser automation; not for browser setup outside WSL2.
---

# WSL2 Browser Setup

Make one browser path work before configuring an automation client:

- **Native WSL Chrome** for interactive browsing, account sign-in, or verifying WSLg browser access.
- **Windows host browser bridge** when a WSL-side tool must control Windows Chrome or Edge over CDP.
- **`agent-browser`** only after either browser path works.

Read [architecture](./references/architecture.md) when choosing a path or diagnosing which layer failed.

## Native WSL Chrome

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh"
```

The script installs Linux Chrome when needed and writes the standard Windows `.wslconfig` networking settings. If it changes `.wslconfig`, have the human run `wsl --shutdown`, reopen WSL, and launch `google-chrome`.

In Chrome, open `chrome://settings/security`, turn `Use secure DNS` fully off, restart Chrome, and verify both a normal external HTTPS site and the target sign-in page.

## Windows Host Browser Bridge

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh"
```

The script launches Windows Edge or Chrome with remote debugging, requests elevation for the port proxy and firewall rule, and waits until WSL2 can reach `/json/version`.

## Optional `agent-browser`

After a browser path works, install the CLI, its downloaded runtime, and the upstream repository when needed:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-agent-browser-runtime.sh"
```

If the user also wants the upstream `vercel-labs/agent-browser` skill package, have the human complete its interactive installer:

```bash
npx skills add vercel-labs/agent-browser
```

For native WSL Chrome, test the client directly:

```bash
agent-browser doctor --offline --quick
agent-browser open https://example.com
agent-browser snapshot -i -c
```

For the Windows host bridge, attach to its CDP endpoint:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/connect-windows-browser.sh" --session windows-host --bridge-port 9333
agent-browser --session windows-host get title
agent-browser --session windows-host snapshot -i -c
```

Use [`setup-agent-browser-wsl2.sh`](./scripts/setup-agent-browser-wsl2.sh) only when a single command should install the runtime, create the Windows bridge, and connect the client.

## Checks And Troubleshooting

Start with non-mutating checks:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-native-wsl-chrome.sh" --check-only
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh" --check-only
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-agent-browser-runtime.sh" --check-only
```

- Read [troubleshooting](./references/troubleshooting.md) when a browser launches but browsing, sign-in, bridge access, or `agent-browser` fails.
- Read [dead ends](./references/dead-ends.md) before attempting lower-level DNS, browser-package, firewall, or client workarounds.
