# Architecture

## Browser Paths And Client Layer

Keep browser availability separate from client behavior even though one skill now owns both.

| Layer | Owns | Does not prove |
| --- | --- | --- |
| Native WSL Chrome | Linux Chrome installation, WSL networking, interactive browsing, and sign-in | That a specific automation client works. |
| Windows host bridge | Launching Windows Chrome or Edge, exposing CDP to WSL2, and verifying `/json/version` | That a specific CDP client can attach and operate correctly. |
| `agent-browser` | CLI/runtime installation and attachment to an established browser path | That the underlying browser or network path is healthy. |

## Native WSL Chrome

Use this first for interactive browsing, profile sign-in, account login flows, or a direct check that WSLg browsing works. The proven path requires Linux `google-chrome`, mirrored WSL networking, DNS tunneling, a full `wsl --shutdown` restart after configuration changes, and Chrome `Use secure DNS` fully off.

## Windows Host Browser Bridge

Use this when a WSL-side tool must drive Windows Chrome or Edge over CDP. The bridge launches the browser with a remote-debugging port, exposes that port to WSL2, and verifies the version endpoint. Any CDP-capable client can then attach.

## `agent-browser`

Test the native path first when Linux Chrome browsing already works. If the client still hangs while manual browsing succeeds, treat it as a client-level failure and use the Windows bridge instead of reopening browser/network diagnosis.
