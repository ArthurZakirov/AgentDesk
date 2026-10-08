<a id="interaction-mode-behavior"></a>
# 🎙️ Interaction mode behavior

These rules govern what the backend agent can do when interaction arrives through Realtime Voice. They do not attempt to instruct a separate frontend speech model that does not receive this `AGENTS.md`.

Frontend-specific conversational pacing belongs on that frontend's own verified prompt or personalization surface. For Codex realtime, AgentDesk maintains those rules in [`codex/realtime-voice-backend-prompt.md`](../../../codex/realtime-voice-backend-prompt.md).

| When | Then |
| --- | --- |
| Interaction mode is confirmed as Realtime Voice, and backend work will be invisible to the user or require noticeable waiting. | Return concise, speakable progress information that the realtime layer can relay: what work started and the next useful result, blocker, or decision. Avoid raw IDs, URLs, prompts, or tool details unless the user needs them. |
| A Realtime Voice request asks for a code walkthrough and the exact repository, worktree, file, line, symbol, or runtime evidence is not already established. | Resolve the concrete location before explaining semantics. Return exact machine/repository/file/line anchors to the realtime layer so it can guide the user through one visible checkpoint at a time. Do not substitute an abstract explanation for missing location evidence. |
| A Realtime Voice request asks for UI navigation and current application state must be inspected to identify the next action. | Inspect the available UI evidence when possible and return only the next grounded destination/action plus the visible state that supports it. Do not manufacture a multi-step click sequence from an unverified UI state. |
| The realtime layer delegates a correction, interruption, changed constraint, or blocking question while backend work is running. | Treat it as active steering. Update or redirect the work immediately when the runtime permits; do not continue executing a superseded plan merely because it began earlier. |
| The interaction is ordinary text or dictated text rather than confirmed Realtime Voice. | Do not impose voice-specific backend packaging; use the structure and completeness appropriate to the request. |
