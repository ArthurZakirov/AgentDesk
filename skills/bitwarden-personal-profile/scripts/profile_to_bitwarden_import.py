#!/usr/bin/env python3
"""Convert personal-profile YAML into Bitwarden Secrets Manager import JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from profile_lib import load_profile, validate_profile


DEFAULT_SECRET_KEY = "ADC_PERSONAL_PROFILE_YAML"
PROJECT_ID = "00000000-0000-0000-0000-000000000001"
SECRET_ID = "00000000-0000-0000-0000-000000000002"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("--output", required=True)
    parser.add_argument("--project-name", default="AgentDesk")
    parser.add_argument("--secret-key", default=DEFAULT_SECRET_KEY)
    parser.add_argument("--no-project", action="store_true", help="Create import JSON without a project association")
    args = parser.parse_args()

    profile_path = Path(args.profile).expanduser()
    profile_text = profile_path.read_text(encoding="utf-8")
    errors = validate_profile(load_profile(str(profile_path)))
    if errors:
        raise SystemExit("; ".join(errors))

    projects = [] if args.no_project else [{"id": PROJECT_ID, "name": args.project_name}]
    project_ids = [] if args.no_project else [PROJECT_ID]
    data = {
        "projects": projects,
        "secrets": [
            {
                "key": args.secret_key,
                "value": profile_text,
                "note": "Personal profile YAML for form filling.",
                "id": SECRET_ID,
                "projectIds": project_ids,
            }
        ],
    }

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        output.chmod(0o600)
    except PermissionError:
        pass
    print(f"Wrote Bitwarden Secrets Manager import JSON: {output}")


if __name__ == "__main__":
    main()
