# Architecture

## Separation Of Concerns

This skill is only about making browser paths usable from WSL2.

It does not choose or configure a specific CDP client. Tool-specific setup belongs in a separate skill.

## Method A: Native WSL Chrome

Use this first when the user wants:

- interactive browsing inside WSL
- profile sign-in
- account login flows
- a quick answer to whether WSLg browsing works at all

This path succeeded once the machine had:

1. Linux `google-chrome`
2. WSL `networkingMode=mirrored`
3. WSL `dnsTunneling=true`
4. a full `wsl --shutdown` restart
5. Chrome `Use secure DNS` fully off

## Method B: Windows Host Browser Bridge

Use this when a tool inside WSL must drive a Windows browser instance over CDP.

The bridge setup is still browser setup rather than client setup:

1. Launch Windows Chrome or Edge with `--remote-debugging-port`
2. Expose that port from Windows to WSL2
3. Verify WSL2 can reach `/json/version`

After that, any CDP-capable client can attach.

## Recommendation

Start with native WSL Chrome for human-interactive sign-in and browsing.

Use the Windows host bridge when a WSL-side automation client specifically needs a Windows browser endpoint.
