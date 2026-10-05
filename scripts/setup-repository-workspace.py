#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ZSH_START = "# >>> AgentDesk repository workspace >>>"
ZSH_END = "# <<< AgentDesk repository workspace <<<"
CURRENT_VARS = (
    "REPOS_DIR",
    "PERSONAL_REPOS_DIR",
    "THIRD_PARTY_REPOS_DIR",
    "PROFESSIONAL_REPOS_DIR",
    "TICKETS_DIR",
)
LEGACY_VARS = ("OPEN_SOURCE_REPOS_DIR",)
ALL_MANAGED_VARS = set(CURRENT_VARS + LEGACY_VARS)


def workspace_paths(home: Path) -> dict[str, Path]:
    repos = home / "Repos"
    return {
        "REPOS_DIR": repos,
        "PERSONAL_REPOS_DIR": repos / "personal",
        "THIRD_PARTY_REPOS_DIR": repos / "third-party",
        "PROFESSIONAL_REPOS_DIR": repos / "professional",
        "TICKETS_DIR": home / "Tickets",
    }


def render_zsh_block() -> str:
    return "\n".join(
        (
            ZSH_START,
            'export REPOS_DIR="$HOME/Repos"',
            'export PERSONAL_REPOS_DIR="$REPOS_DIR/personal"',
            'export THIRD_PARTY_REPOS_DIR="$REPOS_DIR/third-party"',
            'export PROFESSIONAL_REPOS_DIR="$REPOS_DIR/professional"',
            'export TICKETS_DIR="$HOME/Tickets"',
            ZSH_END,
        )
    )


def patch_zshrc(text: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    inside_managed_block = False
    assignment = re.compile(r"^\s*(?:export\s+)?([A-Z0-9_]+)=")

    for line in lines:
        if line.strip() == ZSH_START:
            inside_managed_block = True
            continue
        if inside_managed_block:
            if line.strip() == ZSH_END:
                inside_managed_block = False
            continue

        match = assignment.match(line)
        if match and match.group(1) in ALL_MANAGED_VARS:
            continue
        result.append(line)

    while result and not result[-1].strip():
        result.pop()

    if result:
        result.append("")
    result.extend(render_zsh_block().splitlines())
    return "\n".join(result) + "\n"


def _toml_key(line: str) -> str | None:
    match = re.match(r'^\s*(?:"([^"]+)"|([A-Za-z0-9_-]+))\s*=', line)
    if not match:
        return None
    return match.group(1) or match.group(2)


def render_codex_entries(paths: dict[str, Path]) -> list[str]:
    return [f'{name} = {json.dumps(str(paths[name]))}' for name in CURRENT_VARS]


def patch_codex_config(text: str, paths: dict[str, Path]) -> str:
    lines = text.splitlines()
    result: list[str] = []
    target = "[shell_environment_policy.set]"
    in_target = False
    found_target = False
    inserted = False

    def insert_entries() -> None:
        nonlocal inserted
        if inserted:
            return
        result.extend(render_codex_entries(paths))
        inserted = True

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_target:
                insert_entries()
            in_target = stripped == target
            if in_target:
                found_target = True
            result.append(line)
            continue

        if in_target and _toml_key(line) in ALL_MANAGED_VARS:
            continue
        result.append(line)

    if in_target:
        insert_entries()

    if not found_target:
        while result and not result[-1].strip():
            result.pop()
        if result:
            result.append("")
        result.append(target)
        result.extend(render_codex_entries(paths))

    return "\n".join(result) + "\n"


def migrate_legacy_root(paths: dict[str, Path], dry_run: bool) -> None:
    legacy = paths["REPOS_DIR"] / "open-source"
    target = paths["THIRD_PARTY_REPOS_DIR"]
    if not legacy.exists():
        return
    if not legacy.is_dir():
        raise RuntimeError(f"Legacy path is not a directory: {legacy}")

    children = [child for child in legacy.iterdir() if child.name != ".DS_Store"]
    conflicts = sorted(child.name for child in children if (target / child.name).exists())
    if conflicts:
        raise RuntimeError(
            "Cannot merge legacy open-source directory because these names already "
            f"exist in third-party: {', '.join(conflicts)}"
        )

    if dry_run:
        return

    target.mkdir(parents=True, exist_ok=True)
    for child in children:
        shutil.move(str(child), str(target / child.name))

    ds_store = legacy / ".DS_Store"
    if ds_store.exists():
        ds_store.unlink()
    legacy.rmdir()


def apply(home: Path, dry_run: bool = False) -> None:
    paths = workspace_paths(home)
    migrate_legacy_root(paths, dry_run=dry_run)

    if dry_run:
        print("Repository workspace changes are applicable.")
        return

    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    zshrc = home / ".zshrc"
    original_zshrc = zshrc.read_text() if zshrc.exists() else ""
    updated_zshrc = patch_zshrc(original_zshrc)
    if updated_zshrc != original_zshrc:
        zshrc.write_text(updated_zshrc)

    codex_config = home / ".codex" / "config.toml"
    codex_config.parent.mkdir(parents=True, exist_ok=True)
    original_codex = codex_config.read_text() if codex_config.exists() else ""
    updated_codex = patch_codex_config(original_codex, paths)
    if updated_codex != original_codex:
        codex_config.write_text(updated_codex)

    print("Repository workspace configured.")
    print("Canonical external repository root: third-party")
    print("Codex path variables configured through shell_environment_policy.set.")


def check(home: Path) -> None:
    paths = workspace_paths(home)
    problems: list[str] = []

    for name, path in paths.items():
        if not path.is_dir():
            problems.append(f"{name} directory missing")

    if (paths["REPOS_DIR"] / "open-source").exists():
        problems.append("legacy open-source directory still exists")

    zshrc = home / ".zshrc"
    zsh_text = zshrc.read_text() if zshrc.exists() else ""
    expected_zsh = render_zsh_block()
    if expected_zsh not in zsh_text:
        problems.append("managed zsh repository-workspace block missing or stale")
    if "OPEN_SOURCE_REPOS_DIR" in zsh_text:
        problems.append("legacy OPEN_SOURCE_REPOS_DIR still present in .zshrc")

    codex_config = home / ".codex" / "config.toml"
    codex_text = codex_config.read_text() if codex_config.exists() else ""
    expected_codex = render_codex_entries(paths)
    for entry in expected_codex:
        if entry not in codex_text:
            problems.append(f"Codex config missing {entry.split('=', 1)[0].strip()}")
    if re.search(r'^\s*"?OPEN_SOURCE_REPOS_DIR"?\s*=', codex_text, re.MULTILINE):
        problems.append("legacy OPEN_SOURCE_REPOS_DIR still present in Codex config")

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        raise SystemExit(1)

    print("Repository workspace configuration is valid.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure AgentDesk's canonical repository and ticket workspace layout."
    )
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    home = args.home.expanduser().resolve()
    if args.check:
        check(home)
        return
    apply(home, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
