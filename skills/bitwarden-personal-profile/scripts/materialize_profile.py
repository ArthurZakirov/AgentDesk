#!/usr/bin/env python3
"""Materialize a private personal profile from Bitwarden or a local file."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_PATH = Path.home() / ".config" / "AgentDesk" / "personal-profile.yaml"


def default_output() -> Path:
    return Path(os.environ.get("ADC_PERSONAL_PROFILE_PATH", DEFAULT_PATH))


def read_bitwarden_notes(item: str) -> str:
    if shutil.which("bw") is None:
        raise SystemExit("Bitwarden CLI `bw` is not installed or not on PATH.")
    env = os.environ.copy()
    if not env.get("BW_SESSION"):
        raise SystemExit(
            "BW_SESSION is not set. Run: export BW_SESSION=\"$(bw unlock --raw)\""
        )
    result = subprocess.run(
        ["bw", "get", "notes", item],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "bw get notes failed")
    return result.stdout.strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--from-bitwarden-item", help="Bitwarden item id or name")
    group.add_argument("--from-file", help="Existing YAML/JSON profile file")
    parser.add_argument("--output", default=str(default_output()))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    output = Path(args.output).expanduser()
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {output}")

    if args.from_bitwarden_item:
        content = read_bitwarden_notes(args.from_bitwarden_item)
    else:
        content = Path(args.from_file).expanduser().read_text(encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    try:
        output.chmod(0o600)
    except PermissionError:
        pass

    print(f"Wrote private profile: {output}")
    print(f"export ADC_PERSONAL_PROFILE_PATH={output}")


if __name__ == "__main__":
    main()
