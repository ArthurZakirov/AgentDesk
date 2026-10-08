#!/usr/bin/env python3
"""Install or remove the bedtime guard without replacing unrelated Codex hooks."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from bedtime_guard import clock_now, parse_clock


MANAGED_MARKER = "agentdesk-bedtime-device-guard"
INSTALL_DIR_NAME = "hooks-json/bedtime-device-guard"


def codex_home_from_args(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    env_value = os.environ.get("CODEX_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def read_hooks(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"refusing to modify invalid JSON at {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"refusing to modify non-object JSON at {path}")
    return value


def atomic_json_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = path.with_name(f"{path.name}.bedtime-device-guard.{stamp}.bak")
    counter = 1
    while destination.exists():
        destination = path.with_name(
            f"{path.name}.bedtime-device-guard.{stamp}.{counter}.bak"
        )
        counter += 1
    shutil.copy2(path, destination)
    return destination


def validate_hooks_shape(document: dict[str, object]) -> tuple[dict[str, object], list[object]]:
    hooks = document.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks.json field 'hooks' must be an object")
    groups = hooks.setdefault("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError("hooks.json UserPromptSubmit must be an array")
    return hooks, groups


def is_managed_handler(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    return MANAGED_MARKER in str(value.get("command", "")) or MANAGED_MARKER in str(
        value.get("commandWindows", "")
    )


def remove_managed(groups: list[object]) -> list[object]:
    cleaned: list[object] = []
    for group in groups:
        if not isinstance(group, dict):
            cleaned.append(group)
            continue
        handlers = group.get("hooks")
        if not isinstance(handlers, list):
            cleaned.append(group)
            continue
        had_managed = any(is_managed_handler(handler) for handler in handlers)
        if not had_managed:
            cleaned.append(group)
            continue
        remaining = [handler for handler in handlers if not is_managed_handler(handler)]
        if remaining:
            copied = dict(group)
            copied["hooks"] = remaining
            cleaned.append(copied)
    return cleaned


def quoted(value: Path) -> str:
    return '"' + str(value).replace('"', '\\"') + '"'


def safe_unquoted_windows_arg(value: str) -> str:
    if not value or any(character.isspace() or character in '"&|<>^' for character in value):
        raise ValueError(f"Windows hook path is not safe without quoting: {value}")
    return value


def windows_short_path(path: Path) -> str:
    if os.name != "nt":
        return quoted(path)
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    required = kernel32.GetShortPathNameW(str(path), None, 0)
    if required == 0:
        raise ValueError(f"Windows could not resolve a short path for {path}")
    buffer = ctypes.create_unicode_buffer(required)
    written = kernel32.GetShortPathNameW(str(path), buffer, required)
    if written == 0 or written >= required:
        raise ValueError(f"Windows could not resolve a short path for {path}")
    return safe_unquoted_windows_arg(buffer.value)


def managed_group(script: Path, config: Path) -> dict[str, object]:
    arguments = (
        f"{quoted(script)} --config {quoted(config)} "
        f"--managed-by {MANAGED_MARKER}"
    )
    windows_arguments = (
        f"{windows_short_path(script)} --config {windows_short_path(config)} "
        f"--managed-by {MANAGED_MARKER}"
    )
    return {
        "hooks": [
            {
                "type": "command",
                "command": f"python3 {arguments}",
                "commandWindows": f"py -3 {windows_arguments}",
                "timeoutSec": 2,
                "async": False,
            }
        ]
    }


def install(args: argparse.Namespace) -> int:
    parse_clock(args.start)
    parse_clock(args.end)
    if args.start == args.end:
        raise ValueError("start and end must differ")
    clock_now(args.timezone)

    codex_home = codex_home_from_args(args.codex_home)
    install_dir = codex_home / INSTALL_DIR_NAME
    script_destination = install_dir / "bedtime_guard.py"
    config_destination = install_dir / "config.json"
    hooks_path = codex_home / "hooks.json"

    document = read_hooks(hooks_path)
    hooks, groups = validate_hooks_shape(document)
    legacy_dir = codex_home / "bedtime-device-guard"
    if legacy_dir.exists() and not install_dir.exists():
        install_dir.parent.mkdir(parents=True, exist_ok=True)
        legacy_dir.rename(install_dir)
    install_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).with_name("bedtime_guard.py"), script_destination)
    atomic_json_write(
        config_destination,
        {
            "enabled": True,
            "start": args.start,
            "end": args.end,
            "timezone": args.timezone,
        },
    )
    cleaned = remove_managed(groups)
    cleaned.append(managed_group(script_destination, config_destination))
    hooks["UserPromptSubmit"] = cleaned
    backup_path = backup(hooks_path)
    atomic_json_write(hooks_path, document)

    print(f"Installed bedtime guard in {install_dir}")
    print(f"Updated {hooks_path}")
    if backup_path:
        print(f"Backup: {backup_path}")
    print("Restart Codex, enable hooks if needed, and review/trust the hook.")
    return 0


def uninstall(args: argparse.Namespace) -> int:
    codex_home = codex_home_from_args(args.codex_home)
    hooks_path = codex_home / "hooks.json"
    if hooks_path.exists():
        document = read_hooks(hooks_path)
        hooks, groups = validate_hooks_shape(document)
        cleaned = remove_managed(groups)
        if cleaned:
            hooks["UserPromptSubmit"] = cleaned
        else:
            hooks.pop("UserPromptSubmit", None)
        backup_path = backup(hooks_path)
        atomic_json_write(hooks_path, document)
        print(f"Updated {hooks_path}")
        if backup_path:
            print(f"Backup: {backup_path}")

    install_dir = codex_home / INSTALL_DIR_NAME
    if install_dir.exists():
        shutil.rmtree(install_dir)
        print(f"Removed {install_dir}")
    else:
        print("Bedtime guard was not installed.")
    return 0


def verify(args: argparse.Namespace) -> int:
    codex_home = codex_home_from_args(args.codex_home)
    hooks_path = codex_home / "hooks.json"
    config_path = codex_home / INSTALL_DIR_NAME / "config.json"
    script_path = codex_home / INSTALL_DIR_NAME / "bedtime_guard.py"
    try:
        document = read_hooks(hooks_path)
        _, groups = validate_hooks_shape(document)
        handler_count = sum(
            1
            for group in groups
            if isinstance(group, dict) and isinstance(group.get("hooks"), list)
            for handler in group["hooks"]
            if is_managed_handler(handler)
        )
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("installed config root must be an object")
        parse_clock(str(config.get("start", "")))
        parse_clock(str(config.get("end", "")))
        clock_now(str(config.get("timezone", "local")))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1
    if handler_count != 1:
        print(f"Verification failed: expected one managed handler, found {handler_count}", file=sys.stderr)
        return 1
    if not script_path.is_file():
        print(f"Verification failed: missing {script_path}", file=sys.stderr)
        return 1
    print("Bedtime guard files and hook registration are valid.")
    print("Codex hook enablement and trust must be checked inside Codex.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", help="override the Codex home directory")
    subparsers = parser.add_subparsers(dest="action", required=True)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("--start", required=True, help="blocking start in HH:MM")
    install_parser.add_argument("--end", required=True, help="blocking end in HH:MM")
    install_parser.add_argument("--timezone", default="local")

    subparsers.add_parser("verify")
    subparsers.add_parser("uninstall")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.action == "install":
            return install(args)
        if args.action == "verify":
            return verify(args)
        return uninstall(args)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
