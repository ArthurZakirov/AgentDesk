# Todoist MCP Reference

## Current Setup

Todoist MCP was added globally to Codex on 2026-05-28:

```text
name: todoist
transport: streamable_http
url: https://ai.todoist.net/mcp
```

OAuth login succeeded with:

```bash
codex mcp login todoist
```

Do not inspect auth files or tokens. Use `codex mcp list` and `codex mcp get todoist` for non-secret verification.

Todoist CLI was also installed and authenticated on 2026-05-28:

```bash
npm install -g @doist/todoist-cli
td auth login
td skill install codex
```

The CLI command is `td`, not `todoist`. It authenticated as Arthur's Todoist account and stores its token in the macOS credential manager. The Codex skill installed globally at:

```text
/Users/zakirov/.codex/skills/todoist-cli/SKILL.md
```

Important CLI sandbox note: inside the default Codex filesystem sandbox, `td` may fail to read the macOS credential manager with `AUTH_STORE_READ_FAILED` or `NO_TOKEN`. Running the same `td` command with approved escalation can read the Keychain entry. Do not work around this by printing or exposing Todoist API tokens.

## Tool Routing: MCP vs CLI vs Browser

Use this routing first instead of experimenting.

### Prefer Todoist MCP for

- Creating small batches of tasks when direct MCP tools are visible.
- Updating task titles/content, descriptions, priorities, labels, and other simple metadata.
- Fetching/searching tasks from inside a Codex session when tools are already exposed.
- Non-destructive structured edits where the MCP response directly returns updated task objects.

Known-good example: direct MCP successfully updated the first seven active task titles to emoji-prefixed versions while preserving dates, priorities, descriptions, labels, and project.

### Prefer `td` CLI for

- Verifying current Todoist state in JSON:

```bash
td today --json
td upcoming 7 --json
td task view <task-id> --json --full
```

- Rescheduling an existing task to a new date/time:

```bash
td task reschedule <task-id> 2026-05-29T09:00:00 --json
```

- Diagnosing local Todoist CLI/auth setup:

```bash
td auth status
td doctor
```

Why: MCP rescheduling hit an `Auth required` transport error in this session, while `td task reschedule` successfully moved the 116117 call from 09:30 to 09:00 and Google Calendar reflected the change.

### Prefer Browser for

- Todoist web settings, especially:

```text
Settings -> Calendars
Restore synced calendar
Show events in Todoist
Sync tasks to calendar
```

- Google Calendar visual verification after sync or rescheduling.
- OAuth/login/consent flows where Arthur may need to interact.

Known-good browser workflow: Todoist showed `Task sync calendar: Not found`; clicking `Restore synced calendar` restored the Google Calendar named `Todoist`, after which timed Todoist tasks appeared in Google Calendar.

### Avoid or Treat as Uncertain

- Do not rely on `duration` updates yet. Both `td task update <id> --duration 30m` and MCP duration updates returned success-like responses but left `duration: null`.
- Do not use MCP delete/complete casually. Prior delete/complete attempts were cancelled by the tooling layer, and these actions are destructive or completion-state-changing. Ask Arthur first.
- Do not print or expose Todoist API tokens. If `td` cannot read the macOS credential manager inside the sandbox, rerun the specific `td` command with approved escalation rather than extracting a token.

## Tool Discovery

First try normal tool discovery:

```text
tool_search query: todoist tasks create update list projects
```

If Todoist tools are not visible in the current session, a fresh Codex process may load them. The tested workaround is:

```bash
codex exec --skip-git-repo-check --sandbox read-only "<specific Todoist instruction>"
```

This may need filesystem approval because nested Codex writes to its own state under `~/.codex`.

If direct MCP tools are visible, follow the routing rules above. If they are missing or acting strangely, use `td` for verification and the CLI-preferred operations:

```bash
td auth status
td doctor
td today --json
td upcoming 7 --json
td task view <task-id> --json --full
td task update <task-id> --content "Emoji title" --json
td task reschedule <task-id> 2026-05-29T09:30:00
```

Use `td task update` for title, description, priority, labels, and other normal edits. Use `td task reschedule`, not `td task update --due`, when moving a task to a different date/time and preserving recurrence behavior matters.

## Observed Todoist MCP Actions

The nested Codex session successfully used:

- `todoist/add-tasks`

It surfaced but did not complete because confirmation was cancelled:

- `todoist/delete-object`
- `todoist/complete-tasks`

Treat delete/complete as confirmable/destructive. Ask Arthur before cleanup, bulk completion, deletion, or moving many tasks.

## Known Successful Test

Created a Todoist test task:

```text
Codex MCP test task - delete me
Task ID: 6gjf82JP6mW4p7m7
```

Then created the first active seven:

```text
6gjf8HCRRgPF7q47 — Call 116117 for psychotherapy appointment
6gjf8HGPh67fCCGf — Call bank about missing replacement cards
6gjf8HPfG4H68QW7 — Pay Mom back for MacBook or confirm transfer path
6gjf8HP6RxqvfqV7 — Send first 3 apartment applications
6gjf8HW5GCH95477 — Buy tube and fix both bikes
6gjf8Hhg79r4JR8f — Schedule LinkedIn CEO call
6gjf8HhmXvrHhqg7 — Decide monitor pickup plan
```

The first three were set to `p1` priority. Dates/times used Europe/Berlin local time.

On 2026-05-28, the seven titles were updated to emoji-prefixed versions:

```text
6gjf8HCRRgPF7q47 — 🩺 Call 116117 for psychotherapy appointment
6gjf8HGPh67fCCGf — 💳 Call bank about missing replacement cards
6gjf8HPfG4H68QW7 — 💳 Pay Mom back for MacBook or confirm transfer path
6gjf8HP6RxqvfqV7 — 🏠 Send first 3 apartment applications
6gjf8HW5GCH95477 — 🚲 Buy tube and fix both bikes
6gjf8Hhg79r4JR8f — 💼 Schedule LinkedIn CEO call
6gjf8HhmXvrHhqg7 — 🖥️ Decide monitor pickup plan
```

`td upcoming 7 --json` showed these tasks correctly. In CLI JSON, Todoist priority is numeric: `4` means p1/highest and `1` means p4/default.

## Calendar Sync Observations

Todoist's built-in Google Calendar integration is configured for Arthur's Google account. In Todoist web:

```text
Settings -> Calendars
```

Observed settings on 2026-05-28:

- Google account connected and shown as `Live`.
- `Show events in Todoist` is checked.
- `Sync tasks to calendar` is checked.
- `Sync all-day tasks` is available.
- The external task-sync calendar can appear as `Task sync calendar: Not found` if the Google Calendar named `Todoist` is missing.

When `Task sync calendar` was `Not found`, clicking `Restore synced calendar` in Todoist restored the external Google Calendar named `Todoist`. After a short wait, Todoist showed:

```text
Task sync calendar: Todoist
```

Google Calendar verification on 2026-05-29 showed the Todoist calendar checked and the timed Todoist tasks rendered as events. The four May 29 tasks appeared as 30-minute blocks:

```text
09:30-10:00 — 🩺 Call 116117 for psychotherapy appointment
12:30-13:00 — 💳 Call bank about missing replacement cards
16:00-16:30 — 💼 Schedule LinkedIn CEO call
18:00-18:30 — 💳 Pay Mom back for MacBook or confirm transfer path
```

Attempting to set Todoist task durations with both `td task update <id> --duration 30m` and the Todoist MCP `duration` field returned success-like responses but the task still showed `duration: null`. Despite that, Google Calendar displayed timed tasks as 30-minute events by default. Treat explicit duration support as uncertain in this setup; do not depend on it until re-verified.

## Task Creation Rules

- Create small batches, ideally 1-7 tasks.
- Prefer Inbox unless Arthur has established current Todoist projects.
- Use `p1` only for true Red Zone tasks.
- Put context and "why" in descriptions/comments if supported.
- Use explicit dates when creating tasks from a dated conversation.
- Avoid duplicating tasks already known by title unless Arthur asks for a fresh copy.

## Example Nested Codex Prompt

```text
Use the configured Todoist MCP server. Do not edit local files.
Create exactly these tasks in Todoist Inbox. Today is YYYY-MM-DD and timezone is Europe/Berlin.
Use the emoji-prefixed titles and descriptions below. Report created task IDs.
...
```
