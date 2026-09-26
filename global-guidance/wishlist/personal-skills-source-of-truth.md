# Personal skills source of truth

Migrated from the former machine-global `/Users/zakirov/AGENTS.md`; parked here until reconciled with the current AgentDesk/SkillPort architecture.

- Do not create or edit personal skills directly under `$HOME/.codex/skills`, `$HOME/.claude/skills`, or `$HOME/.agents/skills`. Treat those folders as generated runtime install targets only.
- Personal skills live in domain-specific Git repositories under `$PERSONAL_REPOS_DIR`, usually in each repo's `skills/<skill-name>/SKILL.md` directory.
- Do not hard-code the current list of skill-pack repositories in instructions. Repository names and responsibilities evolve over time.
- Discover current skill-pack repositories at runtime before creating or changing a skill. Prefer the SkillPort manifest at `$PERSONAL_REPOS_DIR/SkillPort/config/skill-repos.local.yaml` when it exists; otherwise inspect `$PERSONAL_REPOS_DIR/*/skills/*/SKILL.md`.
- Choose the source repository by matching the skill's domain to the currently discovered repository purposes, README files, and existing skills.
- When creating or changing a skill, edit the appropriate repo-owned `skills/` directory, then commit and push that repository so every machine can receive the same version.
- Use SkillPort to synchronize skills onto a machine after repo changes or on a new device: run `$PERSONAL_REPOS_DIR/SkillPort/scripts/skillport-sync.sh` from the SkillPort repo. The normal sync path uses the SkillPort manifest and `npx skills` to install/update all configured skill-pack repositories.
- Keep the SkillPort manifest current when adding or removing skill-pack repositories. The local manifest is usually `$PERSONAL_REPOS_DIR/SkillPort/config/skill-repos.local.yaml`.
- Use per-repo `scripts/setup-local-links.sh` only for active local skill development when live edits need to be visible before commit/push. Do not use local symlinks as the normal cross-machine distribution method.
