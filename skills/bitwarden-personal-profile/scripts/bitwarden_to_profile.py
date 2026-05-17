#!/usr/bin/env python3
"""Materialize personal-profile YAML from Bitwarden Secrets Manager data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from profile_lib import DEFAULT_PATH, load_profile, validate_profile


DEFAULT_SECRET_KEY = "ADC_PERSONAL_PROFILE_YAML"


def output_path(value: str | None) -> Path:
    return Path(value or os.environ.get("ADC_PERSONAL_PROFILE_PATH", DEFAULT_PATH)).expanduser()


def extract_secret_value(data: Any, key: str) -> str:
    if isinstance(data, dict) and "secrets" in data:
        candidates = data["secrets"]
    elif isinstance(data, list):
        candidates = data
    else:
        candidates = [data]

    for item in candidates:
        if isinstance(item, dict) and item.get("key") == key and "value" in item:
            return str(item["value"])
    raise SystemExit(f"Secret key not found: {key}")


def run_bws(args: list[str]) -> Any:
    if shutil.which("bws") is None:
        raise SystemExit("Bitwarden Secrets Manager CLI `bws` is not installed or not on PATH.")
    if not os.environ.get("BWS_ACCESS_TOKEN"):
        raise SystemExit("BWS_ACCESS_TOKEN is not set.")
    result = subprocess.run(["bws", *args, "--output", "json"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "bws command failed")
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--from-bitwarden-json", help="Bitwarden Secrets Manager import/export JSON")
    group.add_argument("--from-bws-secret-id", help="Secret id to retrieve with `bws secret get`")
    group.add_argument("--from-bws-project-id", help="Project id to scan with `bws secret list <PROJECT_ID>`")
    parser.add_argument("--secret-key", default=DEFAULT_SECRET_KEY)
    parser.add_argument("--output")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.from_bitwarden_json:
        data = json.loads(Path(args.from_bitwarden_json).expanduser().read_text(encoding="utf-8"))
    elif args.from_bws_secret_id:
        data = run_bws(["secret", "get", args.from_bws_secret_id])
    else:
        data = run_bws(["secret", "list", args.from_bws_project_id])

    profile_text = extract_secret_value(data, args.secret_key)
    out = output_path(args.output)
    if out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(profile_text, encoding="utf-8")
    try:
        out.chmod(0o600)
    except PermissionError:
        pass

    errors = validate_profile(load_profile(str(out)))
    if errors:
        raise SystemExit("; ".join(errors))
    print(f"Wrote private profile: {out}")
    print(f"export ADC_PERSONAL_PROFILE_PATH={out}")


if __name__ == "__main__":
    main()
