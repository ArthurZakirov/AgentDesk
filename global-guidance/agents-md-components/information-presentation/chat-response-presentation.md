<a id="chat-response-presentation"></a>
# 💬 Chat response presentation

Chat-specific visual conventions belong here. Keep medium-independent relevance, anchoring, representation, and visual semantics under the `information-presentation` component group.

| When | Then |
| --- | --- |
| A user turn requires multiple substantive steps, tool calls, or meaningful work before the result is ready. | Use concise in-progress chat updates that begin with `🟡`. Each update should report a meaningful change in state, finding, blocker, or next step rather than narrating every low-level action. |
| The requested work for the turn is complete and control is being handed back to the user. | Send one final response that begins with `🟢`. Make it self-contained: summarize the result, what changed, what was verified, and any remaining blocker or user decision so the user does not need to read the preceding `🟡` updates. |
| Responding after implementing file changes, including a partial or blocked handoff. | Automatically include a clickable link to the verified absolute worktree/checkout root on the computer containing the changes and the exact branch name, without waiting for a request. Obtain both from Git in the checkout actually edited, not the chat's initial directory. Identify the computer when work spans machines and report each affected checkout separately. For detached HEAD, report the verified commit and detached state instead of inventing a branch. For files outside Git, link their absolute containing directory and state that no Git branch applies. Apply the Anchoring rule to changed-file references as well. |
| The turn is simple enough to answer directly without meaningful intermediate work. | Skip `🟡` progress updates and give the result directly; use `🟢` only when it helps distinguish a completed multi-step handoff. |
