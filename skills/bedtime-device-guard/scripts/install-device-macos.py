#!/usr/bin/env python3
"""Install macOS LaunchAgents for the device-level bedtime guard."""

from __future__ import annotations

import argparse
import os
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path

from bedtime_guard import clock_now, parse_clock
from install_guard import atomic_json_write


LABEL_PREFIX = "com.agentdesk.bedtime-device-guard"
ROLES = ("warning", "enforce", "fallback")


def shifted(value: str, delta: int) -> tuple[int, int]:
    parsed = parse_clock(value)
    total = (parsed.hour * 60 + parsed.minute + delta) % (24 * 60)
    return divmod(total, 60)


def plist_document(
    label: str,
    python: Path,
    script: Path,
    config: Path,
    action: str,
    hour: int,
    minute: int,
) -> dict[str, object]:
    return {
        "Label": label,
        "ProgramArguments": [
            str(python),
            str(script),
            action,
            "--platform",
            "macos",
            "--config",
            str(config),
        ],
        "StartCalendarInterval": {"Hour": hour, "Minute": minute},
        "RunAtLoad": True,
        "ProcessType": "Background",
    }


def paths() -> tuple[Path, Path]:
    home = Path.home()
    return (
        home / "Library" / "Application Support" / "AgentDesk" / "bedtime-device-guard",
        home / "Library" / "LaunchAgents",
    )


def launchctl(*arguments: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/bin/launchctl", *arguments],
        capture_output=True,
        text=True,
        check=check,
    )


def unload(plist: Path) -> None:
    launchctl("bootout", f"gui/{os.getuid()}", str(plist))


def install(args: argparse.Namespace) -> int:
    if sys.platform != "darwin":
        raise ValueError("the macOS scheduler installer must run on macOS")
    parse_clock(args.start)
    parse_clock(args.end)
    if args.start == args.end:
        raise ValueError("start and end must differ")
    if not 1 <= args.warning_minutes <= 120:
        raise ValueError("warning-minutes must be from 1 to 120")
    clock_now(args.timezone)
    python = shutil.which("python3")
    if not python:
        raise ValueError("Python 3 is required")

    install_dir, launch_agents = paths()
    install_dir.mkdir(parents=True, exist_ok=True)
    launch_agents.mkdir(parents=True, exist_ok=True)
    source_dir = Path(__file__).parent
    for name in ("bedtime_guard.py", "device_guard.py"):
        shutil.copy2(source_dir / name, install_dir / name)
    config = install_dir / "config.json"
    atomic_json_write(
        config,
        {
            "enabled": True,
            "start": args.start,
            "end": args.end,
            "timezone": args.timezone,
            "warning_minutes": args.warning_minutes,
        },
    )

    schedules = {
        "warning": (*shifted(args.start, -args.warning_minutes), "warn"),
        "enforce": (*shifted(args.start, 0), "enforce"),
        "fallback": (*shifted(args.start, 2), "fallback"),
    }
    for role, (hour, minute, action) in schedules.items():
        label = f"{LABEL_PREFIX}.{role}"
        plist = launch_agents / f"{label}.plist"
        unload(plist)
        with plist.open("wb") as handle:
            plistlib.dump(
                plist_document(
                    label,
                    Path(python),
                    install_dir / "device_guard.py",
                    config,
                    action,
                    hour,
                    minute,
                ),
                handle,
                sort_keys=True,
            )
        launchctl("bootstrap", f"gui/{os.getuid()}", str(plist), check=True)
    print("Installed macOS bedtime warning, shutdown, and logout fallback schedules.")
    return 0


def verify(_args: argparse.Namespace) -> int:
    install_dir, launch_agents = paths()
    missing = []
    for role in ROLES:
        label = f"{LABEL_PREFIX}.{role}"
        plist = launch_agents / f"{label}.plist"
        if not plist.is_file() or launchctl("print", f"gui/{os.getuid()}/{label}").returncode:
            missing.append(role)
    if not (install_dir / "config.json").is_file():
        missing.append("configuration")
    if missing:
        print(f"Verification failed: missing or unloaded: {', '.join(missing)}", file=sys.stderr)
        return 1
    print("All macOS bedtime device jobs are installed and loaded.")
    return 0


def uninstall(_args: argparse.Namespace) -> int:
    install_dir, launch_agents = paths()
    for role in ROLES:
        plist = launch_agents / f"{LABEL_PREFIX}.{role}.plist"
        unload(plist)
        plist.unlink(missing_ok=True)
    if install_dir.exists():
        shutil.rmtree(install_dir)
    print("Removed macOS bedtime device jobs and their local configuration.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)
    installer = subparsers.add_parser("install")
    installer.add_argument("--start", required=True)
    installer.add_argument("--end", required=True)
    installer.add_argument("--timezone", default="local")
    installer.add_argument("--warning-minutes", type=int, default=10)
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
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
