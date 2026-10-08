# Codex Desktop LangSmith Credentials From Bitwarden

Use this setup when Codex Desktop needs LangSmith tracing but the LangSmith API key must remain in Bitwarden Secrets Manager rather than `~/.codex/langsmith.json`, `.env`, or shell startup files.

## Architecture

```text
macOS Keychain
  BWS_ACCESS_TOKEN
        ↓
Bitwarden Secrets Manager
  LANGSMITH_API_KEY
        ↓
LaunchAgent
  com.agentdesk.codex-langsmith-env
        ↓
macOS GUI launch environment
  LANGSMITH_CODEX_API_KEY
        ↓
Codex Desktop → LangSmith tracing plugin
```

The LaunchAgent never writes the LangSmith API key to disk. Its stdout and stderr are `/dev/null`, and the management script reports only whether the GUI environment variable is present.

## Prerequisites

- `bws` is installed.
- The Bitwarden Secrets Manager project available to the service account contains a secret named `LANGSMITH_API_KEY`.
- The BWS access token is already stored in macOS Keychain.
- The LangSmith tracing plugin is installed in Codex.

Keep non-secret tracing configuration in `~/.codex/langsmith.json`, for example:

```json
{
  "enabled": true,
  "api_url": "https://eu.api.smith.langchain.com",
  "project": "codex"
}
```

Do not add `api_key` to that file.

## Install

Run the repository script with the Keychain account that owns the existing `BWS_ACCESS_TOKEN` item:

```bash
BWS_KEYCHAIN_ACCOUNT="<keychain-account>" \
  ./scripts/manage-codex-langsmith-env.sh install
```

The installer copies itself to `~/.local/libexec/agentdesk/`, creates `~/Library/LaunchAgents/com.agentdesk.codex-langsmith-env.plist`, bootstraps the LaunchAgent, and lets `RunAtLoad` populate the GUI environment.

The installed plist contains only non-secret paths and identifiers. At runtime the script:

1. reads `BWS_ACCESS_TOKEN` from macOS Keychain without printing it;
2. invokes `bws run` with output suppressed;
3. checks that `LANGSMITH_API_KEY` exists inside the injected process;
4. writes only that value to the GUI launch environment as `LANGSMITH_CODEX_API_KEY`;
5. clears the shell variable holding the BWS access token before exiting.

`LANGSMITH_CODEX_API_KEY` is used instead of the generic variable so the secret is scoped to the Codex LangSmith integration.

## Verify

Use the management script; it never prints the value:

```bash
./scripts/manage-codex-langsmith-env.sh status
```

Expected shape:

```text
LaunchAgent: loaded
LANGSMITH_CODEX_API_KEY: present (value hidden)
```

For a lower-level presence check that still does not reveal the value:

```bash
[[ -n "$(launchctl getenv LANGSMITH_CODEX_API_KEY)" ]] \
  && echo "LangSmith credential is available to newly launched GUI apps"
```

After installation or refresh, fully quit and reopen Codex Desktop. Existing GUI processes do not retroactively inherit environment changes.

Then create a new Codex turn and verify the trace in the configured LangSmith project.

## Refresh And Remove

After rotating the Bitwarden secret:

```bash
./scripts/manage-codex-langsmith-env.sh refresh
```

To remove the setup and clear the GUI environment variable:

```bash
./scripts/manage-codex-langsmith-env.sh uninstall
```

## Security Notes

- Never use `bws secret list` for this workflow.
- Never print `LANGSMITH_API_KEY`, `LANGSMITH_CODEX_API_KEY`, or `BWS_ACCESS_TOKEN`.
- Never place a secret value directly in shell command arguments or launchd plist files.
- Keep the LangSmith endpoint and project in the JSON config because they are not credentials.
- The LaunchAgent intentionally sends stdout and stderr to `/dev/null` so secret-manager diagnostics cannot leak into persistent logs.
- `launchctl setenv` stores the credential only in the logged-in user's launchd environment, not on disk. Newly launched processes in that GUI session can potentially inherit or query it, so this is process-environment isolation rather than Codex-only secret storage.
- The Codex-specific variable name reduces accidental use by unrelated integrations but is not an access-control boundary.

## Reproduce Current State

These commands regenerate the non-secret state described above:

```bash
./scripts/manage-codex-langsmith-env.sh status

python3 - <<'PY'
import json
from pathlib import Path

config = json.loads((Path.home() / ".codex" / "langsmith.json").read_text())
print("api_key_present=", "api_key" in config)
print("enabled=", bool(config.get("enabled")))
print("endpoint=", config.get("api_url"))
print("project=", config.get("project"))
PY
```

The exact values can drift as configuration changes. Re-run the commands rather than treating this document as the source of truth.
