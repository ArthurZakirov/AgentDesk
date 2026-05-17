#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from profile_lib import load_profile, normalize_language_values, profile_path, validate_profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--language", choices=["en", "de"], default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = profile_path(args.path)
    data = load_profile(str(path))
    errors = validate_profile(data)
    if errors:
        raise SystemExit("; ".join(errors))
    normalized = normalize_language_values(data, args.language)
    if args.json:
        print(json.dumps(normalized, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"Loaded profile: {path}")


if __name__ == "__main__":
    main()
