# Dead Ends

These were explored and did not shorten the path to success.

## `dbus-x11`

Not required for the final working setup.

## Ubuntu `chromium-browser`

Not required for the final working setup.

It is often a Snap wrapper on Ubuntu and is not the default recommendation here.

## Low-Level DNS Or Firewall Surgery First

Do not start by changing random DNS files, browser flags, or firewall rules by hand.

The shortest real path was:

1. mirrored WSL networking
2. `dnsTunneling=true`
3. `wsl --shutdown`
4. Secure DNS fully off in Chrome

Use the bridge helper if a Windows-host browser endpoint is needed.

## Treating Every Chrome Console Message As A Root Cause

Many shell messages looked scary but were not blockers.

Focus on:

- whether `google-chrome` opens
- whether `https://example.com` loads
- whether a real target site and sign-in page load interactively
- whether the Windows bridge responds on `/json/version`

Those checks mattered more than the console noise.
