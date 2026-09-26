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

## Newly captured candidates

- **Investigate before interrupting stakeholders** — desired system outcome: reduce avoidable stakeholder interruptions by exhausting proportionate self-service evidence first. Needs explicit operationalization of what counts as a stakeholder, what evidence sources are available, how much investigation is proportionate, and when a human decision/context request remains necessary.
- **Do not generalize around unanswered questions** — desired behavior: when an answer is pending, avoid speculative flexibility that may later be discarded. Needs a reliable distinction between dependent vs. independent work and between reversible minimal implementation vs. premature abstraction.
- **Prefer concrete diff review for internal code choices** — desired workflow: avoid asking the user to choose between hypothetical implementation structures when observable behavior is equivalent; instead produce the smallest maintainable concrete diff unless the choice creates material cost, risk, or irreversibility. Needs validation across repo workflows and review tooling.
- **Push coherent work before review / draft-PR workflow** — environment-specific desired workflow. Keep parked until repository authorization rules, default reviewers, CI behavior, `git review`, worktree handling, and cross-repository validation have been verified for the target environment.
- **Work from inside the repo** — desired harness/session behavior because relative links, diffs, and commands depend on cwd. Keep parked until the exact semantics of `EnterWorktree`, session cwd changes, and multi-repo handling are verified for each supported harness.
