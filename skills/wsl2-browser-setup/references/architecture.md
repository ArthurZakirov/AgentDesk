# Architecture

## Layered Model

Prove the lowest relevant layer before debugging the next one:

1. **WSL networking:** mirrored networking, DNS tunneling, and any required WSL restart.
2. **Browser path:** native Linux Chrome or a Windows browser exposed over CDP.
3. **Automation client:** optional `agent-browser` runtime and connection.

A working interactive browser does not prove that an automation client works, and a client failure does not by itself mean the browser path is broken.

## Native WSL Chrome

Use this path for:

- interactive browsing inside WSL
- profile or account sign-in
- confirming that WSLg browsing works
- native `agent-browser` launch attempts

The proven setup combines Linux `google-chrome`, `networkingMode=mirrored`, `dnsTunneling=true`, a full `wsl --shutdown` restart, and Chrome `Use secure DNS` fully off.

## Windows Host Browser Bridge

Use this path when a WSL-side tool must drive Windows Chrome or Edge over CDP:

1. Launch the Windows browser with a remote-debugging port.
2. Expose that port from Windows to WSL2.
3. Verify that WSL2 can reach `/json/version`.
4. Attach the requested CDP client.

The bridge is client-independent. `agent-browser` is one possible client, not part of the bridge itself.

## `agent-browser`

The optional client layer owns:

- installing the CLI and downloaded browser runtime
- cloning `vercel-labs/agent-browser` when requested
- testing native WSL browser control
- attaching to an existing Windows host bridge

When native manual browsing succeeds but `agent-browser` hangs, test the client layer or use the Windows bridge instead of repeating browser installation and networking changes.
