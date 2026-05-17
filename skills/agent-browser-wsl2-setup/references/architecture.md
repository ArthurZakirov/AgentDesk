# Architecture

## Separation Of Concerns

`$wsl2-browser-setup` owns browser availability.

This skill owns:

- installing `agent-browser`
- running `agent-browser install`
- cloning the `vercel-labs/agent-browser` repo
- attaching `agent-browser` to a browser path that already exists

## Browser Modes

### Native WSL browser mode

Use this when manual Linux Chrome browsing inside WSL2 already works.

That path is good for trying native `agent-browser` launch and snapshot commands first, but it should be treated as a client-level test rather than a browser-setup test.

### Windows host bridge mode

Use this when a Windows browser endpoint is already exposed to WSL2 over CDP.

This path is browser-client-agnostic up until the final attach step. The browser skill creates the bridge; this skill only attaches `agent-browser` to it.

## Recommendation

Do browser repair in `$wsl2-browser-setup`.

Do `agent-browser` install and attach logic here.
