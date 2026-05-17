#!/usr/bin/env python3
"""Create or update the personal profile secret through the bws CLI."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from profile_lib import load_profile, validate_profile


DEFAULT_SECRET_KEY = "ADC_PERSONAL_PROFILE_YAML"


def run_bws(args: list[str]) -> Any:
    if shutil.which("bws") is None:
        raise SystemExit("Bitwarden Secrets Manager CLI `bws` is not installed or not on PATH.")
    if not os.environ.get("BWS_ACCESS_TOKEN"):
        raise SystemExit("BWS_ACCESS_TOKEN is not set.")
    result = subprocess.run(["bws", *args, "--output", "json"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "bws command failed")
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def find_existing(project_id: str, key: str) -> dict[str, Any] | None:
    secrets = run_bws(["secret", "list", project_id])
    if not isinstance(secrets, list):
        return None
    for secret in secrets:
        if isinstance(secret, dict) and secret.get("key") == key:
            return secret
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("--project-id", default=os.environ.get("BWS_PERSONAL_PROFILE_PROJECT_ID"))
    parser.add_argument("--secret-key", default=DEFAULT_SECRET_KEY)
    parser.add_argument("--create-duplicates", action="store_true", help="Always create instead of editing an existing key")
    args = parser.parse_args()

    if not args.project_id:
        raise SystemExit("Provide --project-id or set BWS_PERSONAL_PROFILE_PROJECT_ID.")

    profile_path = Path(args.profile).expanduser()
    errors = validate_profile(load_profile(str(profile_path)))
    if errors:
        raise SystemExit("; ".join(errors))
    profile_text = profile_path.read_text(encoding="utf-8")

    existing = None if args.create_duplicates else find_existing(args.project_id, args.secret_key)
    if existing:
        result = run_bws(
            [
                "secret",
                "edit",
                existing["id"],
                "--key",
                args.secret_key,
                "--value",
                profile_text,
                "--note",
                "Personal profile YAML for form filling.",
                "--project-id",
                args.project_id,
            ]
        )
        print(f"Updated Bitwarden secret: {result.get('id', existing['id'])}")
    else:
        result = run_bws(
            [
                "secret",
                "create",
                args.secret_key,
                profile_text,
                args.project_id,
                "--note",
                "Personal profile YAML for form filling.",
            ]
        )
        print(f"Created Bitwarden secret: {result.get('id')}")


if __name__ == "__main__":
    main()
