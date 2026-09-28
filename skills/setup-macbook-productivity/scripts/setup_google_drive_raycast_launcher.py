#!/usr/bin/env python3
"""Create a Raycast-friendly launcher for Google Drive on macOS."""

from __future__ import annotations

import plistlib
import shutil
import subprocess
from pathlib import Path


GOOGLE_DRIVE_APP = Path("/Applications/Google Drive.app")
LAUNCHER_APP = Path.home() / "Applications/Google Drive Launcher.app"
BUNDLE_ID = "com.arthur.google-drive-launcher"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=check, text=True, capture_output=True)


def ensure_macos() -> None:
    if not Path("/System/Library/CoreServices/SystemVersion.plist").exists():
        raise RuntimeError("This script only supports macOS.")


def ensure_google_drive() -> None:
    if not GOOGLE_DRIVE_APP.exists():
        raise RuntimeError("Google Drive is not installed in /Applications.")

def write_launcher_bundle() -> None:
    contents = LAUNCHER_APP / "Contents"
    macos = contents / "MacOS"
    resources = contents / "Resources"
    macos.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)

    info = {
        "CFBundleName": "Google Drive Launcher",
        "CFBundleDisplayName": "Google Drive Launcher",
        "CFBundleIdentifier": BUNDLE_ID,
        "CFBundleVersion": "1",
        "CFBundleShortVersionString": "1.0",
        "CFBundlePackageType": "APPL",
        "CFBundleExecutable": "launcher",
        "CFBundleIconFile": "GoogleDrive.icns",
        "LSUIElement": True,
    }
    with (contents / "Info.plist").open("wb") as handle:
        plistlib.dump(info, handle)

    executable = macos / "launcher"
    executable.write_text(
        '#!/bin/zsh\n/usr/bin/open "/Applications/Google Drive.app"\nexit 0\n',
        encoding="utf-8",
    )
    executable.chmod(0o755)

    icon_candidates = [
        GOOGLE_DRIVE_APP / "Contents/Resources/gdrive.icns",
        GOOGLE_DRIVE_APP / "Contents/Resources/drive.icns",
    ]
    for icon in icon_candidates:
        if icon.exists():
            shutil.copy2(icon, resources / "GoogleDrive.icns")
            break

    subprocess.run(("touch", str(LAUNCHER_APP)), check=True)
    subprocess.run(
        ("mdimport", str(LAUNCHER_APP)),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def verify_launchservices() -> bool:
    result = run("open", "-Ra", "Google Drive Launcher", check=False)
    return result.returncode == 0


def exercise_launcher() -> None:
    subprocess.run(
        ("open", str(LAUNCHER_APP)),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def main() -> int:
    try:
        ensure_macos()
        ensure_google_drive()
        write_launcher_bundle()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Setup failed: {exc}")
        return 1

    if not verify_launchservices():
        print("Launcher was created, but LaunchServices cannot resolve it by name yet.")
        print("Open it once from ~/Applications, then restart Raycast.")
        return 2

    exercise_launcher()
    print(f"Created: {LAUNCHER_APP}")
    print("LaunchServices can resolve 'Google Drive Launcher'.")
    print("Raycast/Spotlight can now launch this app from the normal search workflow.")
    print("The launcher reopens /Applications/Google Drive.app without a terminal workflow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
