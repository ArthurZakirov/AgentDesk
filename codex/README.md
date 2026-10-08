# 🎙️ Codex realtime voice configuration

Codex realtime voice has a conversational model in front of the backend agent. The realtime layer does not receive backend `AGENTS.md` guidance before it delegates, so behavior that must apply before delegation needs a realtime-specific control surface.

Codex exposes the experimental top-level `experimental_realtime_ws_backend_prompt` setting for that surface. The setting replaces the bundled realtime backend prompt; it is not an append-only instruction field. Keep the complete prompt in Markdown and generate the loaded TOML value from it rather than maintaining a second escaped copy by hand.

## 🗂️ Files

| File | Role |
| --- | --- |
| [`realtime-voice-backend-prompt.md`](realtime-voice-backend-prompt.md) | Canonical editable realtime prompt. It starts from OpenAI's bundled prompt and adds the AgentDesk control layer. |
| [`../scripts/render-codex-config.py`](../scripts/render-codex-config.py) | Replaces one `__AGENTDESK_REALTIME_BACKEND_PROMPT__` marker in a template and atomically writes the active `config.toml`. |

## ⚙️ Local layout

Keep these machine-local files under `$CODEX_HOME` (normally `~/.codex`):

1. `config.template.toml` — editable config template containing exactly one unquoted `__AGENTDESK_REALTIME_BACKEND_PROMPT__` marker as the value of `experimental_realtime_ws_backend_prompt`.
2. `realtime-voice-backend-prompt.md` — editable prompt source.
3. `render-config.py` — renderer copied from AgentDesk.
4. `config.toml` — generated config consumed by the runtime.

Render after changing either source:

```bash
~/.codex/render-config.py
```

The renderer writes through a temporary file and then replaces `config.toml`, so a partial write does not leave the active config truncated.

## 🔄 Runtime boundary

The prompt controls the realtime conversational layer before backend delegation. Backend `AGENTS.md`, skills, tools, and project context apply after work reaches the backend agent; they cannot retroactively govern a spoken response produced entirely by the realtime layer.

This applies to Codex-backed product surfaces that load the same local Codex configuration. Do not assume an unrelated voice implementation or remote client uses this file without verifying that surface.

## 🔎 Upstream evidence

* [Codex config source](https://github.com/openai/codex/blob/main/codex-rs/config/src/config_toml.rs) defines `experimental_realtime_ws_backend_prompt` as the realtime websocket instruction override.
* [Bundled realtime prompt](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/realtime/backend_prompt.md) is the baseline copied into the canonical AgentDesk prompt.
* [Codex issue #37950](https://github.com/openai/codex/issues/37950) documents the runtime distinction: realtime startup excludes `AGENTS.md`, while this override reaches the conversational layer.
