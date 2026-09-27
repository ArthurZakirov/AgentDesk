#!/usr/bin/env python3
"""Regenerate global AGENTS.md entrypoints from the canonical layered sources."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    agentdesk_root = script_dir.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--agents-home", dest="codex_home", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--claude-home", type=Path)
    parser.add_argument("--opencode-home", type=Path)
    parser.add_argument("--replace-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    command = [
        sys.executable,
        str(script_dir / "bootstrap-agents-md.py"),
        "--manifest", str(agentdesk_root / "global-guidance" / "agents-md-manifest.yaml"),
    ]
    if args.codex_home:
        command += ["--codex-home", str(args.codex_home.expanduser())]
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
