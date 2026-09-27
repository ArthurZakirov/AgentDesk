# 🧭 Problem intent before a proposed solution

## Desired outcome

When the user gives an implementation command in solution-space language, the agent should remain alert to the underlying outcome. If the proposed mechanism is likely invalid, suboptimal, brittle, or based on a questionable assumption, the agent should surface the inferred intent, investigate established alternatives, and offer the better route before implementing the proposal blindly.

The purpose is not to turn every direct command into a consultation or approval dialogue. The desired behavior must preserve the user's ability to give straightforward instructions while detecting the cases in which following the literal mechanism would fail to achieve the apparent goal.

## Motivating example

The user asked for a generated global `AGENTS.md` to be placed directly under `/Users/zakirov/` instead of inside `.codex`. The unspoken goal was cross-agent portability: Codex, OpenCode, OpenClaw, and future agent harnesses should all discover the same global guidance.

The proposed filesystem location was the user's own attempted solution to that portability problem. It relied on the assumption that every harness would traverse parent folders and recognize the same instruction filename and scope. The agent implemented the requested location, but Codex could not consume it as intended.

A better interaction would have been approximately:

> It sounds as though your real goal is one shared source of global instructions that several agent harnesses can consume. A home-directory `AGENTS.md` may not be discovered by all of them. I will first verify each harness's actual discovery rules and look for an established source-of-truth-plus-generated-adapters design. If that fits your goal, should I implement it instead of relying on parent-folder discovery?

The wording is illustrative; the implementation mechanism remains undecided.

## Desired decision pattern

Before implementing a user-prescribed mechanism, consider:

1. What outcome appears to motivate this request?
2. Which assumptions must be true for the proposed mechanism to achieve it?
3. Can those assumptions be checked cheaply through documentation, inspection, or a small experiment?
4. Is there an established solution that achieves the outcome more reliably?
5. Would the alternative materially change scope, cost, risk, reversibility, or user intent?

If the literal request is sound and low-risk, execute it without unnecessary ceremony. If evidence reveals a material mismatch, explain the mismatch and ask about the outcome-changing alternative before implementing it. Do not silently substitute a materially different solution.

## Boundaries to preserve

- A command can be both intentional and specific; do not assume every concrete instruction is an uninformed guess.
- Do not force the user to restate every request in problem-space language.
- Prefer a concrete, evidence-backed objection over generic pushback or speculative “better ideas.”
- Do not add a blocking clarification when the intent and safe corrective path are obvious and materially equivalent.
- Do not expand the task merely because a broader architecture would be theoretically cleaner.
- When the inferred intent is uncertain or the alternative changes the requested outcome, expose the inference and let the user decide.

## Open design questions

- What observable signals distinguish a user-selected constraint from a mistaken solution hypothesis?
- How large must the expected benefit or avoided failure be before the agent interrupts execution?
- Can the agent state its inferred intent and continue with reversible research without blocking, then ask only when a decision becomes material?
- How should this interact with explicit commands such as “do exactly this,” time-sensitive work, and expert users who already evaluated alternatives?
- How can success be measured without producing chronic clarification fatigue or paternalistic behavior?
- Should the system help the user build a parallel habit of articulating goals, or should intent recovery remain entirely the agent's responsibility?

## Promotion test

Evaluate a mixed set of direct commands:

- commands whose proposed mechanism is correct and should execute immediately;
- commands based on a verifiably false assumption;
- commands with a better but materially different alternative;
- commands where the user deliberately chose a non-default mechanism;
- commands whose underlying goal cannot be inferred reliably.

The behavior passes only if it catches consequential solution–goal mismatches while leaving ordinary direct execution fast and preserving the user's final choice.
