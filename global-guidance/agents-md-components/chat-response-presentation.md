<a id="chat-response-presentation"></a>
# 💬 Chat response presentation

Chat-specific visual conventions belong here. Keep medium-independent relevance, anchoring, representation, and visual semantics under the `information-presentation` component group.

| When | Then |
| --- | --- |
| A user turn requires multiple substantive steps, tool calls, or meaningful work before the result is ready. | Use concise in-progress chat updates that begin with `🟡`. Each update should report a meaningful change in state, finding, blocker, or next step rather than narrating every low-level action. |
| The requested work for the turn is complete and control is being handed back to the user. | Send one final response that begins with `🟢`. Make it self-contained: summarize the result, what changed, what was verified, and any remaining blocker or user decision so the user does not need to read the preceding `🟡` updates. |
| The turn is simple enough to answer directly without meaningful intermediate work. | Skip `🟡` progress updates and give the result directly; use `🟢` only when it helps distinguish a completed multi-step handoff. |
| Interaction mode is confirmed as Realtime Voice, and an explanation requires the user to inspect a file, line, symbol, image, interface, or unfamiliar term before later information will be useful. | Enter an interactive micro-step mode: briefly announce the pacing when helpful, give exactly one actionable instruction, concept, observation, or dependency, then stop speaking and yield. Continue only after the user confirms, asks a question, or otherwise signals readiness; answer that question at the current layer before resuming the larger path. |
| The interaction is ordinary text or dictated text rather than confirmed Realtime Voice, or the spoken explanation imposes no meaningful inspection or dependency checkpoint. | Do not force micro-step pacing; use the amount of structure and completeness appropriate to the request. |
