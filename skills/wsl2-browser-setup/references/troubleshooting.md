# Troubleshooting

## `google-chrome` opens but external sites fail

Do these in order:

1. Ensure Windows `.wslconfig` contains:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
```

2. Run `wsl --shutdown`
3. Reopen WSL
4. Open `chrome://settings/security`
5. Turn `Use secure DNS` fully `Off`

## `Use secure DNS` looks disabled but still says `OS default (when available)`

That is still enabled.

The actual toggle must be off.

## A normal site works but the target sign-in flow still acts strange in headless tests

Use the interactive browser as the ground truth for browser setup success.

If the target site opens and the sign-in page renders correctly in an interactive Chrome window, treat the browser setup itself as working.

Any remaining failure may belong to the specific automation client rather than the browser path.

## Shell shows noisy Chrome errors

These were harmless in this setup:

- `dbus ... UPower ... ServiceUnknown`
- `Created TensorFlow Lite XNNPACK delegate for CPU`
- `Registration response error message: DEPRECATED_ENDPOINT`
- `Registration URL fetching failed`

Do not treat those as the root cause by default.

## Windows host bridge is not reachable from WSL2

Check these in order:

1. The Windows browser is running with the requested remote debugging port
2. The Windows elevation step completed
3. `http://HOST_IP:BRIDGE_PORT/json/version` responds from WSL2

If the bridge still is not reachable, rerun the bridge setup script before changing anything lower level.
