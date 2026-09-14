# Codex hook contract

Verified against OpenAI Codex `main` at commit `d76109773497850ed2699f2816e3f7b1867d0c14` on 2026-09-14.

Primary-source locations:

- [`ConfiguredHookHandler`](https://github.com/openai/codex/blob/d76109773497850ed2699f2816e3f7b1867d0c14/codex-rs/app-server-protocol/src/protocol/v2/config.rs) defines command handlers, including `command`, `commandWindows`, `timeoutSec`, and `async`.
- [`user_prompt_submit.rs`](https://github.com/openai/codex/blob/d76109773497850ed2699f2816e3f7b1867d0c14/codex-rs/hooks/src/events/user_prompt_submit.rs) shows that a trusted `UserPromptSubmit` handler returning `decision: block` with a non-empty `reason` stops the prompt.
- [The generated input schema](https://github.com/openai/codex/blob/d76109773497850ed2699f2816e3f7b1867d0c14/codex-rs/hooks/schema/generated/user-prompt-submit.command.input.schema.json) confirms that command hooks receive JSON on standard input.
- [The generated output schema](https://github.com/openai/codex/blob/d76109773497850ed2699f2816e3f7b1867d0c14/codex-rs/hooks/schema/generated/user-prompt-submit.command.output.schema.json) documents the accepted output fields.

The installed handler uses this shape:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \".../bedtime_guard.py\" --config \".../config.json\"",
            "commandWindows": "py -3 C:\\...\\bedtime_guard.py --config C:\\...\\config.json",
            "timeoutSec": 2,
            "async": false
          }
        ]
      }
    ]
  }
}
```

During the blocked window, the hook writes this structure to standard output and exits successfully:

```json
{"decision":"block","reason":"Bedtime guard is active. Capture the thought offline and rest; Codex is available again after the configured end time."}
```

During allowed hours it writes nothing and exits successfully. It consumes standard input but does not parse, copy, store, or log the prompt.

The hook must stay synchronous. An asynchronous pre-submit hook cannot be relied on to stop submission before the model request.

On Windows, the installer resolves the installed files to space-free short paths and emits no embedded command quotes. This avoids the current `cmd.exe /C` outer-quoting failure affecting quoted `commandWindows` paths. Installation stops with a clear error if Windows cannot provide safe space-free paths.
