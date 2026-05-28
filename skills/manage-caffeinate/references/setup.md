# Launchd-Backed Caffeinate Setup

## What This Skill Manages

The skill manages a macOS launchd job named `agentdesk-caffeinate` that runs:

```bash
/usr/bin/caffeinate -dimsu
```

Despite the label, the behavior is not Codex-specific. It is a machine-level keep-awake assertion useful for Codex, Claude Code, terminals, dev servers, browser automation, downloads, and other local processes.

## Why Launchd

Starting `caffeinate` with a background shell command such as:

```bash
nohup caffeinate -dimsu &
```

can be fragile from agent-run shell sessions. The process can exit when the shell/session wrapper ends, and PID capture can be unreliable depending on how the command is quoted.

Using launchd makes macOS own the process:

```bash
launchctl submit -l codex-caffeinate -- /usr/bin/caffeinate -dimsu
```

This creates a launchd job with the label `agentdesk-caffeinate` and the program arguments:

```text
/usr/bin/caffeinate
-dimsu
```

## Initial Setup Performed

The initial experiment used the temporary label `codex-caffeinate`:

```bash
launchctl submit -l codex-caffeinate -- /usr/bin/caffeinate -dimsu
```

It was verified with:

```bash
launchctl list codex-caffeinate
pmset -g assertions
```

The packaged AgentDesk skill now uses the label `agentdesk-caffeinate`, and it removes the old `codex-caffeinate` label when turning caffeinate on or off.

Expected `launchctl list agentdesk-caffeinate` output includes a `PID`, `Program = "/usr/bin/caffeinate"`, and `ProgramArguments` containing `-dimsu`.

Expected `pmset -g assertions` output includes `caffeinate command-line tool` assertions such as:

```text
PreventUserIdleSystemSleep
PreventUserIdleDisplaySleep
PreventSystemSleep
PreventDiskIdle
```

## Stop Command

Turn the behavior off with:

```bash
launchctl remove codex-caffeinate
```

For the packaged skill label:

```bash
launchctl remove agentdesk-caffeinate
```

## Flag Meaning

- `-d`: prevent display idle sleep.
- `-i`: prevent system idle sleep.
- `-m`: prevent disk idle sleep.
- `-s`: prevent system sleep when on AC power.
- `-u`: declare user activity.

## Lid-Close Caveat

`caffeinate` prevents idle sleep while macOS honors the assertion. Closing a MacBook lid can still force sleep unless the Mac is in a supported clamshell setup, usually plugged into power with external display/input.
