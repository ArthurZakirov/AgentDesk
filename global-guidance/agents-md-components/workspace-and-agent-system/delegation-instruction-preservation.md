<a id="delegation-instruction-preservation"></a>
# 🤝 Delegation and instruction preservation

When delegating work to another agent, harness, or execution environment:

1. **Preserve intent and constraints.** Preserve the original task intent and all applicable instructions, including user-provided instructions and conversation context, `AGENTS.md` files, relevant skills, repository-specific guidance, and other authoritative configuration.
2. **Prevent instruction drift.** Do not introduce restrictions, permissions, or workflow defaults that contradict applicable instructions or silently replace them with generic defaults.
3. **Preserve source access.** Identify the authoritative instruction sources and direct the receiving agent to inspect them before execution. Do not assume it automatically receives instructions or files accessible to the delegating agent; transmit essential constraints explicitly when source access is unavailable.
4. **Handle conflicts explicitly.** If delegation requires changing a constraint, make the change explicit and respect the applicable instruction hierarchy. Do not silently substitute a different rule.

Before dispatch, compare the outgoing request with the applicable workflow rules—especially Git commit/push policy, validation, safety, and output requirements. See SystemSmith's `engineer-agentic-ai` skill for the delegation validation method.
