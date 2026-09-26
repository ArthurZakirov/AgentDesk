#!/usr/bin/env python3
"""Regenerate global AGENTS.md entrypoints from the canonical layered sources."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import platform as platform_module
import subprocess
import sys


def detect_platform() -> str:
    system = platform_module.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows-wsl"
    if system == "linux":
        release = platform_module.release().lower()
        version = platform_module.version().lower()
        if "microsoft" in release or "microsoft" in version:
            return "windows-wsl"
    raise SystemExit("Unsupported platform; pass --platform explicitly")


def default_private_context_root(agentdesk_root: Path) -> Path:
    configured = os.environ.get("PRIVATE_CONTEXT_ROOT")
    if configured:
        return Path(configured).expanduser()
    return agentdesk_root.parent / "AgentDesk-private-context"


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    agentdesk_root = script_dir.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-context-root", type=Path)
    parser.add_argument("--platform", choices=("macos", "windows-wsl"))
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--claude-home", type=Path)
    parser.add_argument("--opencode-home", type=Path)
    parser.add_argument("--replace-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    private_root = (args.private_context_root or default_private_context_root(agentdesk_root)).expanduser().resolve()
    target_platform = args.platform or detect_platform()
    overlay_name = "macos.md" if target_platform == "macos" else "windows-wsl.md"

    command = [
        sys.executable,
        str(script_dir / "bootstrap-agents-md.py"),
        "--common", str(agentdesk_root / "agent-guidance" / "common.md"),
        "--overlay", str(agentdesk_root / "agent-guidance" / overlay_name),
        "--platform", target_platform,
        "--registry", str(private_root / "skillport" / "repositories.json"),
    ]
    if args.codex_home:
        command += ["--codex-home", str(args.codex_home)]
    if args.claude_home:
        command += ["--claude-home", str(args.claude_home)]
    if args.opencode_home:
        command += ["--opencode-home", str(args.opencode_home)]
    if args.replace_existing:
        command.append("--replace-existing")
    if args.dry_run:
        command.append("--dry-run")

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
