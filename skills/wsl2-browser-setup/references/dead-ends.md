# Dead Ends

## Adding Browser Packages Before Proving The Short Path

`dbus-x11` and Ubuntu `chromium-browser` were not required for the working setup. Ubuntu's `chromium-browser` is often a Snap wrapper and is not the default here.

## Starting With Low-Level DNS Or Firewall Surgery

For native Chrome, start with mirrored networking, DNS tunneling, a WSL restart, and Secure DNS fully off. For a Windows endpoint, use the bridge helper before making manual firewall edits.

## Treating Console Noise As The Root Cause

Focus on observable behavior:

- Does `google-chrome` open?
- Do normal HTTPS pages and the real sign-in page load?
- Does the bridge respond on `/json/version`?
- Can the selected client attach after the browser path works?

## Repeating Browser Repair For A Client Failure

If manual Chrome browsing works but `agent-browser` hangs, debug the client layer or switch it to the Windows bridge. Do not reinstall Chrome or repeat networking changes without new browser-layer evidence.

## Treating The Windows Bridge As Client-Specific

The Windows host bridge is a generic CDP endpoint. Keep bridge validation separate from the behavior of any one client, including `agent-browser`.

## Using The Combined Wrapper By Default

The combined `setup-agent-browser-wsl2.sh` helper is convenient for a full Windows-bridge setup, but the separate browser and client checks reveal failures more clearly. Prefer the smallest helper that matches the requested layer.
