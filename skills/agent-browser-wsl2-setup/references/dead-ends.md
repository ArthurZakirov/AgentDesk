# Dead Ends

These are the coupling mistakes this split is meant to avoid.

## Mixing Browser Repair With Client Repair

If `google-chrome` itself does not browse correctly, fix that in `$wsl2-browser-setup`.

If `google-chrome` browses correctly but `agent-browser` still hangs, do not assume the browser setup is still broken.

## Installing Browsers From The Agent-Browser Skill

This skill should not own Linux Chrome install, WSL networking mode, or Windows port proxy setup as first-class setup steps.

Those belong in the browser skill.

## Treating The Windows Bridge As Agent-Browser-Specific

The Windows host bridge is a generic CDP exposure mechanism.

`agent-browser` is only one possible client that can attach to it.

## Repeating The Old One-Shot Wrapper By Default

The compatibility wrapper still exists, but it is not the clearest path anymore.

Use the split skills unless backward compatibility matters more than clarity.
