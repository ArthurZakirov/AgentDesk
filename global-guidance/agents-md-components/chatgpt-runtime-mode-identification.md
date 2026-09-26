<a id="chatgpt-runtime-mode"></a>
# 🧭 ChatGPT runtime mode identification

Before applying mode-dependent guidance, identify these dimensions from trustworthy runtime or app metadata:

| Dimension | Possible result | Fallback when not identified |
| --- | --- | --- |
| Client or surface | Android ChatGPT app, macOS desktop app, Windows desktop app, browser, or another reported client | Keep it `unknown`. |
| Product mode | Ordinary ChatGPT Chat, ChatGPT Work, or Codex | Unless Work or Codex is positively identified, treat it as ordinary Chat for mode-dependent guidance. |
| Interaction mode | Realtime voice or ordinary text input, whether typed or dictated | Make a tentative, message-scoped inference from style only when runtime metadata is unavailable. |

Use the following evidence order:

1. Prefer runtime or app metadata whenever it is available.
2. Without metadata, use style only as a low-confidence fallback for the current message:
   - Many spelling, grammar, or punctuation mistakes can suggest typed input.
   - Polished grammar can be consistent with dictation or realtime voice, but does not distinguish them by itself.
   - An abruptly unfinished thought or pause can weakly suggest realtime voice; a self-contained thought is more consistent with dictation or typing.
3. Treat these signals as probabilities, not proof. Do not make safety-sensitive or irreversible decisions from them, and leave client or product details `unknown` when they lack evidence.
4. Reassess interaction mode for each new message. A conversation can move between voice, dictation, and typing; do not treat a chat's previous mode as permanent.

Apply only the guidance relevant to the evidence available for the current mode.

After identifying the product mode, read exactly the matching mode-specific file before applying mode-dependent behavior. Do not preload the other mode files.

| Product mode | Required mode-specific guidance |
| --- | --- |
| Ordinary ChatGPT Chat | [agents-md-references/chatgpt-chat.md](agents-md-references/chatgpt-chat.md) |
| ChatGPT Work | [agents-md-references/chatgpt-work.md](agents-md-references/chatgpt-work.md) |
| Codex | [agents-md-references/codex.md](agents-md-references/codex.md) |


At the start of every new conversation, make the runtime identification visible to Arthur in the first assistant response:

- Briefly state the identified client or surface, product mode, and interaction mode before or alongside the normal response.
- Explicitly distinguish confirmed metadata from tentative inference, and say `unknown` for dimensions that cannot be identified reliably.
- Briefly state the concrete mode-dependent guidance that will be followed because of that identification; mention only rules that materially affect the current conversation.
- If Arthur's first message is only a greeting, use this runtime report instead of a generic "How can I help?"-style prompt. A concise greeting may precede it.
- If the first message already contains a substantive request, keep the runtime report concise and continue directly with the requested work in the same response.
- Reassess later messages as required above, but do not repeat the full runtime report on every turn unless the identified mode changes or Arthur asks for it.
