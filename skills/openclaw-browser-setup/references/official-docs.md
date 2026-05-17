# Official OpenClaw Browser References

Use this file when you need the official basis for a setup or troubleshooting step. Keep SKILL.md terse; load this file only when a browser issue appears.

## 1. CLI browser quick start

Source:
- https://docs.openclaw.ai/cli/browser

Why it mattered:
- It defined the minimum proof loop used for local validation.

Relevant passage:

```text
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Other useful points from the same page:
- `openclaw` launches an OpenClaw-managed isolated Chrome instance.
- `user` controls the existing signed-in Chrome session through Chrome DevTools MCP.
- If `plugins.allow` is present, it must include `browser` or the CLI subcommand can disappear.

## 2. Browser tool overview, plugin control, and profile model

Source:
- https://docs.openclaw.ai/tools/browser

Why it mattered:
- It explained the managed `openclaw` profile, the attached `user` profile, the browser plugin requirements, and the loopback security model.

Relevant passages:

```text
OpenClaw can run a dedicated Chrome/Brave/Edge/Chromium profile that the agent controls.
```

```text
The default browser experience needs both:
- plugins.entries.browser.enabled not disabled
- browser.enabled=true
```

```text
If plugins.allow is set, browser.enabled=true is not enough by itself.
```

```text
Browser control is loopback-only; access flows through the Gateway’s auth or node pairing.
```

Useful takeaways:
- Use `openclaw` by default for isolated automation.
- Use `user` only when an existing logged-in local browser session matters.
- Restart the gateway after browser config changes so the browser service re-registers.

## 3. Gateway troubleshooting runbook for pairing and browser failures

Source:
- https://docs.openclaw.ai/gateway/troubleshooting

Why it mattered:
- It mapped the exact failure signatures that appeared locally.

Relevant passages:

```text
PAIRING_REQUIRED | Device identity is known but not approved for this role.
Approve pending request: openclaw devices list then openclaw devices approve <requestId>.
```

```text
Browser tool fails:
openclaw browser status
openclaw browser start --browser-profile openclaw
openclaw browser profiles
openclaw logs --follow
openclaw doctor
```

```text
Failed to start Chrome CDP on port → browser process failed to launch.
```

Useful takeaways:
- Fix pairing before browser internals when auth is failing.
- Check plugin allowlists, executable path, and local Chrome availability in that order.

## 4. Control UI device pairing and scope-upgrade behavior

Source:
- https://docs.openclaw.ai/web/control-ui

Why it mattered:
- The local gateway was returning `pairing required`, and the device request was a scope-upgrade style approval.

Relevant passages used:
- New browser or device connections can show `disconnected (1008): pairing required`.
- The approval flow is `openclaw devices list` followed by `openclaw devices approve <requestId>`.
- If the browser retries with changed role, scopes, or public key, the old pending request can be replaced by a new `requestId`.
- Moving from read access to write or admin access is treated as an approval upgrade, not a silent reconnect.

Operational takeaway:
- Re-run `openclaw devices list` immediately before approval if the pairing state is changing under you.

## 5. Linux browser troubleshooting for CDP startup failures

Source:
- https://docs.openclaw.ai/tools/browser-linux-troubleshooting

Why it mattered:
- The managed browser initially failed to launch on this Linux host.

Relevant passages:

```text
Failed to start Chrome CDP on port 18800 for profile "openclaw".
```

```text
"browser": {
  "enabled": true,
  "executablePath": "/usr/bin/google-chrome-stable",
  "headless": true,
  "noSandbox": true
}
```

```text
"browser": {
  "enabled": true,
  "attachOnly": true,
  "headless": true,
  "noSandbox": true
}
```

Useful takeaways:
- Prefer a real Chrome binary over snap Chromium when managed launch is failing.
- On server-style Linux hosts, headless mode is the default fix path.
- If managed launch is impossible, use `attachOnly` with a manually started browser or remote CDP.
