<a id="chatgpt-runtime-mode"></a>
# 🧭 ChatGPT runtime mode identification

## Identify the runtime

**When**

- Before applying guidance whose behavior depends on the ChatGPT client, product mode, or interaction mode.

**Then**

- Identify the following dimensions from trustworthy runtime or app metadata when available:

| Dimension | Possible result | Fallback when not identified |
| --- | --- | --- |
| Client or surface | Android ChatGPT app, macOS desktop app, Windows desktop app, browser, or another reported client | Keep it `unknown`. |
| Product mode | Ordinary ChatGPT Chat, ChatGPT Work, or Codex | Unless Work or Codex is positively identified, treat it as ordinary Chat for mode-dependent guidance. |
| Interaction mode | Realtime voice or ordinary text input, whether typed or dictated | Make only a tentative, message-scoped inference from style when runtime metadata is unavailable. |

- Prefer runtime/app metadata over inference.
- If metadata is unavailable, treat style signals as low-confidence probabilities only; never use them for safety-sensitive or irreversible decisions.

## Load mode-specific guidance

**When**

- Product mode has been identified or resolved by the fallback above.

**Then**

- Read exactly the matching mode-specific file before applying mode-dependent behavior; do not preload the others.

| Product mode | Required mode-specific guidance |
| --- | --- |
| Ordinary ChatGPT Chat | [agents-md-references/chatgpt-chat.md](agents-md-references/chatgpt-chat.md) |
| ChatGPT Work | [agents-md-references/chatgpt-work.md](agents-md-references/chatgpt-work.md) |
| Codex | [agents-md-references/codex.md](agents-md-references/codex.md) |

## First response of a conversation

**When**

- Producing the first assistant response in a new conversation.

**Then**

- Briefly state the identified client/surface, product mode, and interaction mode.
- Distinguish confirmed metadata from tentative inference and say `unknown` when a dimension cannot be identified reliably.
- Mention only mode-dependent guidance that materially affects the current conversation.
- If the first message is only a greeting, use this runtime report instead of a generic help prompt; if it contains a substantive request, keep the report concise and continue directly with the task.

## Later messages

**When**

- A new user message arrives after the first response.

**Then**

- Reassess interaction mode because voice, dictation, and typing can change within one conversation.
- Do not repeat the full runtime report unless the identified mode changes or the user asks for it.
