# 🧪 Agent behavior problem space and wishlist

This file preserves desired behavior and open questions that are **not yet validated as reliable runtime mechanisms**. It is deliberately excluded from the generated global `AGENTS.md`.

Promote an item into the canonical guidance only after the responsible runtime behavior and the wording that controls it have both been verified.

## 🌐 Browser execution and responsive coordination

The following wishes were removed from the global guidance because they describe preferred outcomes, not confirmed control mechanisms:

- Run browser and Computer Use work directly when the necessary capabilities are available; do not delegate merely because a browser is involved.
- Delegate only when the user explicitly requests it or a validated task or skill mechanism requires scoped parallel work.
- Create or fork a separate Codex task only when the user requests it or a confirmed product requirement makes it necessary.
- Do not create a persistent Goal merely to observe a browser operation or wait for a worker, unless Goal mode is explicitly requested or required.
- For independent authorized work, provide a dispatch update and prefer asynchronous completion signals over repeated blocking waits.
- During voice work, distinguish the speaking coordinator from the execution agent; do not recursively delegate merely because a request originated in voice.
- When a runtime restriction prevents direct execution or timely steering, report the observed restriction and its scope without guessing at a platform-wide cause.

## 🔬 Validation questions

- Which product mechanisms create or require Goals, task delegation, and new Codex chats?
- Which instructions are actually honored by each supported runtime, and which merely express intent?
- What observable evidence proves that a replacement rule changes the relevant behavior?

## 🍎 macOS overlay wishes

These rules were removed from the active global `AGENTS.md` and parked here pending a clearer need for platform-specific global guidance:

- Use this Mac's native checkout paths from its permission-restricted machine configuration. Do not reuse path values from another physical computer or infer them from shared guidance.
- The global Codex `AGENTS.md` on this machine is generated from the common rules plus a platform layer. Do not replace it with a link to a single cross-platform source.
- SkillPort's macOS LaunchAgent owns unattended safe refresh, guidance composition, and remote skill installation. Keep its concrete roots and executable paths in the local launchd environment, not in shared files or interactive shell startup files.
- Claude and OpenCode entrypoints may reference the same canonical layers through their supported native mechanisms. Preserve unrelated local configuration and do not treat those references as Codex import syntax.
