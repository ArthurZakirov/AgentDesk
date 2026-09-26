# 🍎 macOS overlay wishes

These rules were removed from active global guidance and are parked here pending a clearer need for platform-specific global guidance.

- Use this Mac's native checkout paths from its permission-restricted machine configuration. Do not reuse path values from another physical computer or infer them from shared guidance.
- The global Codex `AGENTS.md` on this machine is generated from the configured components plus a platform layer. Do not replace it with a link to a single cross-platform source.
- SkillPort's macOS LaunchAgent owns unattended safe refresh, guidance composition, and remote skill installation. Keep its concrete roots and executable paths in the local launchd environment, not in shared files or interactive shell startup files.
- Claude and OpenCode entrypoints may reference the same canonical layers through their supported native mechanisms. Preserve unrelated local configuration and do not treat those references as Codex import syntax.
