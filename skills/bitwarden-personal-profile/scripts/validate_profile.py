#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from profile_lib import load_profile, profile_path, validate_profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()

    path = profile_path(args.path)
    data = load_profile(str(path))
    errors = validate_profile(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Profile is valid: {path}")


if __name__ == "__main__":
    main()
