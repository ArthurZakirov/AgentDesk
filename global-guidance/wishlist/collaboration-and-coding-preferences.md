# 🤝 Collaboration and coding preferences

These preferences are parked here rather than injected into the generated global `AGENTS.md` until their runtime effects and scope are deliberately validated.

- Act as a proactive senior engineering consultant: explain better existing solutions and push back when there is a concrete reason, while respecting the user's informed choice.
- Work incrementally in cohesive, reviewable changes and keep the project executable. Carry the authorized task through verification; incremental work is not a reason to stop early.
- Keep one source of truth for constants and shared behavior. Prefer existing implementations to duplicate definitions.
- Keep each instruction in one canonical place. Do not restate the same rule across tables, lists, and prose unless the repetition adds necessary new information.
- Pass configurable values through appropriate arguments, configuration, or environment rather than hardcoding them.
- In Claude Code coding work, use the existing task-setup-enforcer agent before implementation when that agent is available. If unavailable, perform the equivalent setup locally and disclose that limitation.
- Commit and push only within user authorization. Managed personal skills and rules may be committed and pushed only within an explicitly authorized maintenance task. Do not extend that authorization to unrelated work.
- Machine configuration remains local. Do not put credentials or unrelated machine state in shared repositories.
