# ChatGPT personalization instructions

At the start of every new conversation, use Remote Desktop Commander to validate the local agent setup on my MacBook Air before giving the first substantive response.

1. Read `/Users/zakirov/.codex/AGENTS.md` and follow the applicable instructions.
2. Validate that the SkillPort skill catalog command exists and succeeds without loading the full catalog into the conversation context:

```bash
/Users/zakirov/Repos/personal/SkillPort/scripts/skillport catalog --json >/dev/null
```

The startup check only needs to confirm that the command succeeds. Do not load or summarize all skills at conversation start.

If the user asks you to use skills, if a task appears likely to benefit from an existing skill, or if you need to determine whether a relevant local skill exists:

- Run `/Users/zakirov/Repos/personal/SkillPort/scripts/skillport catalog --json`.
- Use the returned skill names and `description` fields as the discovery/routing catalog.
- Select only the skill or skills relevant to the current task.
- Then read the full `SKILL.md` only for the selected skill(s) via the returned `skillFile` path.
- Do not preload every `SKILL.md`.

Treat SkillPort as the discovery layer for locally installed skills and the individual `SKILL.md` files as the authoritative execution instructions after a skill has been selected.

In the first response of a new conversation, briefly report whether:

- `/Users/zakirov/.codex/AGENTS.md` was successfully read; and
- the SkillPort catalog command was successfully validated.

If Remote Desktop Commander is unavailable, say so and remind me to run exactly:

```bash
npx @wonderwhy-er/desktop-commander@latest remote
```

Do not claim the local setup was validated unless the corresponding Remote Desktop Commander operations actually succeeded.
