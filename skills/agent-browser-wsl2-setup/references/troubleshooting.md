# Troubleshooting

## `agent-browser` is missing

Run the runtime installer:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/agent-browser-wsl2-setup/scripts/setup-agent-browser-runtime.sh"
```

## Native `agent-browser` still hangs even though manual Chrome browsing works

Treat that as an `agent-browser` runtime issue, not a browser-setup issue.

If browser setup was already proven by `$wsl2-browser-setup`, switch to the Windows host bridge mode instead of repeating low-level Chrome debugging here.

## `connect-windows-browser.sh` fails

Make sure the generic browser bridge is already reachable from WSL2:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/wsl2-browser-setup/scripts/setup-windows-host-browser-bridge.sh" --check-only
```

If `/json/version` is not reachable, go back to `$wsl2-browser-setup`.

## `npx skills add vercel-labs/agent-browser` blocks progress

That step is interactive and belongs to the human.

The AI should handle the non-interactive install steps before or after that point.
