#!/usr/bin/env python3
"""Generate a deterministic Raycast Quick Links import for local Git repositories.

The hand-maintained Raycast quicklinks.json is intentionally never read or
written by this script.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import tempfile


# User-configurable settings.
RAYCAST_DIR = Path.home() / ".config" / "raycast"
OUTPUT_FILENAME = "repositories-quicklinks.json"
PROTECTED_FILENAME = "quicklinks.json"
REPOSITORY_ROOT_ENV_VARS = (
    "PERSONAL_REPOS_DIR",
    "OPEN_SOURCE_REPOS_DIR",
)
OPEN_WITH = "Visual Studio Code"

def configured_repository_roots() -> list[Path]:
    """Resolve repository roots from configured environment variables."""
    roots: list[Path] = []
    seen: set[str] = set()

    for variable in REPOSITORY_ROOT_ENV_VARS:
        raw = os.environ.get(variable)
        if not raw:
            continue

        root = Path(raw).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError(f"{variable} must point to a directory: {root}")

        key = str(root)
        if key not in seen:
            roots.append(root)
            seen.add(key)

    if not roots:
        variables = ", ".join(REPOSITORY_ROOT_ENV_VARS)
        raise ValueError(f"None of the configured repository variables are set: {variables}")

    return roots


def find_repositories(roots: list[Path]) -> list[Path]:
    """Return immediate child directories that are Git repositories."""
    repositories: dict[str, Path] = {}

    for root in roots:
        for candidate in root.iterdir():
            if (
                candidate.is_dir()
                and not candidate.name.startswith(".")
                and (candidate / ".git").exists()
            ):
                resolved = candidate.resolve()
                repositories[str(resolved)] = resolved

    return sorted(
        repositories.values(),
        key=lambda path: (path.name.casefold(), str(path).casefold()),
    )


def build_entries(repositories: list[Path]) -> list[dict[str, str]]:
    return [
        {
            "name": f"{repository.name} — VS Code",
            "link": str(repository),
            "openWith": OPEN_WITH,
        }
        for repository in repositories
    ]


def protected_quicklinks_path() -> Path:
    return (RAYCAST_DIR / PROTECTED_FILENAME).expanduser().resolve()


def default_output_path() -> Path:
    return (RAYCAST_DIR / OUTPUT_FILENAME).expanduser().resolve()


def ensure_safe_output(output: Path) -> Path:
    output = output.expanduser().resolve()
    if output == protected_quicklinks_path():
        raise ValueError("The hand-maintained Raycast quicklinks.json cannot be an output")
    return output


def write_import(output: Path, entries: list[dict[str, str]], dry_run: bool = False) -> None:
    output = ensure_safe_output(output)
    result = (json.dumps(entries, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

    print(f"repositories: {len(entries)} Quick Links")
    if dry_run:
        print(f"Would write: {output}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    lock_path = output.with_name(output.name + ".lock")

    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        previous = output.read_bytes() if output.exists() else None

        if previous == result:
            print(f"Unchanged: {output}")
            return

        if previous is not None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            backup = output.with_name(f"{output.name}.bak.{stamp}")
            with backup.open("xb") as saved:
                os.chmod(backup, 0o600)
                saved.write(previous)
                saved.flush()
                os.fsync(saved.fileno())
            print(f"Previous generated import backed up: {backup}")

        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=output.parent,
                prefix=output.name + ".",
                delete=False,
            ) as file:
                temporary = Path(file.name)
                file.write(result)
                file.flush()
                os.fsync(file.fileno())

            current = output.read_bytes() if output.exists() else None
            if current != previous:
                raise ValueError("Output changed during generation; refusing to overwrite")

            os.replace(temporary, output)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    print(f"Import file: {output}")


def generate(output: Path | None = None, dry_run: bool = False) -> None:
    roots = configured_repository_roots()
    repositories = find_repositories(roots)
    entries = build_entries(repositories)
    write_import(output or default_output_path(), entries, dry_run=dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a separate Raycast Quick Links import from repository roots "
            "configured through environment variables. The hand-maintained "
            "quicklinks.json stays untouched."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"Generated import file (default: {default_output_path()})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show repository count and output path without writing files",
    )
    args = parser.parse_args()

    try:
        generate(args.output, args.dry_run)
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(
            1,
            f"Generation stopped ({type(error).__name__}): {error}\n",
        )


if __name__ == "__main__":
    main()
