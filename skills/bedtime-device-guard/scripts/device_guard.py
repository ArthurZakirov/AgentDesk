#!/usr/bin/env python3
"""Native warning, shutdown, and logout actions with live time guards."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import time
from pathlib import Path

from bedtime_guard import clock_now, evaluate, load_config, parse_clock


def minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def warning_due(config: dict[str, object], now_override: str | None = None) -> bool:
    warning = config.get("warning_minutes", 10)
    start_value = config.get("start")
    timezone_name = config.get("timezone", "local")
    if not isinstance(warning, int) or isinstance(warning, bool) or not 1 <= warning <= 120:
        raise ValueError("warning_minutes must be an integer from 1 to 120")
    if not isinstance(start_value, str) or not isinstance(timezone_name, str):
        raise ValueError("start and timezone must be strings")
    current = clock_now(timezone_name, now_override).time().replace(tzinfo=None)
    until_start = (minutes(parse_clock(start_value)) - minutes(current)) % (24 * 60)
    return 0 < until_start <= warning


def run_quiet(command: list[str]) -> bool:
    try:
        return subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
    except OSError:
        return False


def warn(platform: str) -> int:
    message = "Computer access ends soon. Save your work and begin the shutdown routine."
    if platform == "macos":
        script = f'display notification "{message}" with title "Bedtime device guard"'
        return 0 if run_quiet(["/usr/bin/osascript", "-e", script]) else 1
    return 0 if run_quiet(["msg.exe", "*", message]) else 1


def enforce(platform: str) -> int:
    if platform == "macos":
        return 0 if run_quiet(
            ["/usr/bin/osascript", "-e", 'tell application "System Events" to shut down']
        ) else 1
    return 0 if run_quiet(["shutdown.exe", "/s", "/f", "/t", "0"]) else 1


def fallback(platform: str) -> int:
    if platform != "macos":
        return 0
    # This job runs shortly after the shutdown request. If the Mac is still in
    # the blocked window and still has a GUI session, force that session out.
    return 0 if run_quiet(["/bin/launchctl", "reboot", "logout"]) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("warn", "enforce", "fallback", "check"))
    parser.add_argument("--platform", choices=("macos", "windows"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--now", help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config)
        if args.action == "warn":
            due = warning_due(config, args.now)
        else:
            due = evaluate(config, args.now)
    except ValueError as error:
        print(f"bedtime-device-guard: {error}", file=sys.stderr)
        return 2
    if not due:
        return 0
    if args.action == "warn":
        return warn(args.platform)
    if args.action == "enforce":
        return enforce(args.platform)
    if args.action == "fallback":
        return fallback(args.platform)
    print("active")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
