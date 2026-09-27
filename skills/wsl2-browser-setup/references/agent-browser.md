# `agent-browser`

Use this client layer only after either native Linux Chrome works for real browsing or the Windows host bridge responds on `/json/version`.

## Runtime Setup

Run:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-agent-browser-runtime.sh"
```

The script installs missing apt prerequisites and the `agent-browser` CLI, runs `agent-browser install`, and clones `vercel-labs/agent-browser` when absent. Use its flags to skip work that the current machine does not need.

If the user also wants the upstream reusable skill, the human must complete its interactive installer:

```bash
npx skills add vercel-labs/agent-browser
```

Do not pause the non-interactive runtime setup merely because that optional interactive step remains.

## Native WSL Browser

When manual Linux Chrome browsing works, test the client directly:

```bash
agent-browser doctor --offline --quick
agent-browser open https://example.com
agent-browser snapshot -i -c
```

If these commands hang while manual Chrome remains healthy, switch to the Windows bridge rather than changing the proven browser setup.

## Windows Host Browser Bridge

After the generic bridge is reachable, attach the client:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/connect-windows-browser.sh" --session windows-host --bridge-port 9333
agent-browser --session windows-host get title
agent-browser --session windows-host snapshot -i -c
```

## One-Shot Compatibility Flow

[`../scripts/setup-agent-browser-wsl2.sh`](../scripts/setup-agent-browser-wsl2.sh) combines runtime setup, Windows bridge setup, and client attachment. Keep it for the older one-shot flow; prefer the individual scripts when diagnosing a specific layer.
