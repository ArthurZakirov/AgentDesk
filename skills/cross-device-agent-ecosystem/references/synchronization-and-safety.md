# Synchronization and public-safety rules

Use this reference for cross-machine repository refresh, skill installation,
global guidance composition, automation status, and publication decisions.

## Sources of truth

| Material | Canonical source | Generated or installed result |
| --- | --- | --- |
| Repository content | Its remote GitHub repository, reconciled through a local checkout | Per-machine working tree |
| Agent skills | Repository `skills/` directories selected by the SkillPort registry | Shared global `~/.agents/skills` installation used by Codex and OpenCode, including the ChatGPT desktop app's host-side Codex agent, with Claude Code aliases where supported |
| Global guidance | One private common layer plus the relevant macOS or Windows/WSL platform overlay | Concrete harness-specific global instructions rendered by SkillPort tooling |

Never maintain separate editable skill copies for Codex, Claude Code, or
OpenCode. Edit the canonical repository source, review it, then reinstall the
explicit configured remote subset.

Use the cross-tool environment variables `SKILLPORT_ROOT` and
`AGENTDESK_ROOT` to locate AgentDesk global guidance and its repository registry.
Do not publish or hardcode machine-specific checkout locations.

## Refresh automation

The durable refresh job may:

- fetch repositories and apply safe fast-forward pulls;
- render global guidance from the private common layer plus the current platform
  overlay; and
- reinstall the explicit remote skill subset selected by the registry.

It must never stage or commit files.

Status distinctions matter:

- macOS automation has been verified to run at login/load and on a 15-minute
  cadence;
- the intended Windows design uses Task Scheduler at logon and every 15 minutes
  with `StartWhenAvailable`;
- do not claim Windows scheduling is verified merely because the design or task
  definition exists.

When checking Windows, verify separately that the task exists, its triggers and
`StartWhenAvailable` match the design, its configured roots resolve, the latest
run completed successfully, and the expected repositories/guidance/skills were
refreshed. Record observed evidence and remaining unknowns rather than promoting
an intended state to a verified fact.

## Optional push policy

Automatic pushes are registry-scoped and fail closed:

- private repositories require verified private visibility and a credential
  scan;
- public repositories require an exact reviewed-HEAD approval and a
  personal-data scan;
- unknown or unverifiable visibility blocks the push; and
- missing metadata or failed checks skip pushing without blocking safe refresh.

Refresh permission does not authorize staging, committing, or pushing. Treat
those as distinct mutations requiring their own authorization and applicable
review.

## Public skill boundary

Public AgentDesk material may include reputation-positive, high-level device
models, operating systems, roles, and interface architecture. Exclude any detail
that would enable account, network, host, or identity targeting, including:

- residential or private-life details;
- account identifiers, authentication state, passwords, tokens, credentials,
  key material, or host fingerprints;
- IP addresses, usernames, configured hostnames, private network coordinates,
  or machine-specific absolute paths;
- unpublished applications, career drafts, or other unrelated private records.

Never inspect credential-capable files to perform a public-content review. Scan
only the changed public files and report category-level pass/fail results without
printing suspected secret values.
