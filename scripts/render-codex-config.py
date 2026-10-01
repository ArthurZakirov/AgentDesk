#!/usr/bin/env python3
"""Render Codex config.toml from a template plus the realtime voice prompt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROMPT_TOKEN = "__AGENTDESK_REALTIME_BACKEND_PROMPT__"


def parse_args() -> argparse.Namespace:
    home = Path.home() / ".codex"
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, default=home / "config.template.toml")
    parser.add_argument("--prompt", type=Path, default=home / "realtime-voice-backend-prompt.md")
    parser.add_argument("--output", type=Path, default=home / "config.toml")
    return parser.parse_args()


def render(template: str, prompt: str) -> str:
    count = template.count(PROMPT_TOKEN)
    if count != 1:
        raise ValueError(f"expected exactly one {PROMPT_TOKEN} marker, found {count}")
    # JSON string syntax is valid TOML basic-string syntax for this content and
    # safely escapes newlines, quotes, and backslashes.
    return template.replace(PROMPT_TOKEN, json.dumps(prompt, ensure_ascii=False))


def main() -> None:
    args = parse_args()
    template = args.template.expanduser()
    prompt = args.prompt.expanduser()
    output = args.output.expanduser()

    rendered = render(
        template.read_text(encoding="utf-8"),
        prompt.read_text(encoding="utf-8"),
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(rendered, encoding="utf-8")
    temporary.replace(output)


if __name__ == "__main__":
    main()
