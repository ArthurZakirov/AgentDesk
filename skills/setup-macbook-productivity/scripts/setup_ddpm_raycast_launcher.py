#!/usr/bin/env python3
"""Build the DDPM launcher; does not grant permissions or launch the UI."""
from __future__ import annotations

import argparse
import plistlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BUNDLE_ID = "local.arthur.ddpm-launcher"
DDPM = Path("/Applications/DDPM/DDPM.app")


def install(output: Path) -> None:
    if sys.platform != "darwin":
        raise RuntimeError("This installer requires macOS.")
    if not DDPM.is_dir():
        raise RuntimeError("Install Dell Display and Peripheral Manager from Dell first.")
    if not shutil.which("xcrun"):
        raise RuntimeError("Apple Command Line Tools are required to compile the launcher.")
    source = Path(__file__).with_name("ddpm_launcher.swift")
    output = output.expanduser().absolute()
    if output.is_symlink():
        raise RuntimeError("Refusing to replace a symlink.")
    if output.exists():
        info = plistlib.loads((output / "Contents/Info.plist").read_bytes())
        if info.get("CFBundleIdentifier") != BUNDLE_ID:
            raise RuntimeError("Refusing to overwrite an unrelated application.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ddpm-build-", dir=output.parent) as temp:
        bundle = Path(temp) / output.name
        contents = bundle / "Contents"
        macos = contents / "MacOS"
        resources = contents / "Resources"
        macos.mkdir(parents=True)
        resources.mkdir()
        subprocess.run(["xcrun", "swiftc", str(source), "-o", str(macos / "launcher")], check=True)
        icon = DDPM / "Contents/Resources/AppIcon.icns"
        if icon.exists():
            shutil.copy2(icon, resources / "DDPM.icns")
        info = {
            "CFBundleIdentifier": BUNDLE_ID,
            "CFBundleName": "DDPM Launcher",
            "CFBundleDisplayName": "DDPM Launcher",
            "CFBundleExecutable": "launcher",
            "CFBundlePackageType": "APPL",
            "CFBundleVersion": "1",
            "CFBundleShortVersionString": "1.0",
            "CFBundleIconFile": "DDPM",
            "LSUIElement": True,
            "NSHighResolutionCapable": True,
        }
        (contents / "Info.plist").write_bytes(plistlib.dumps(info))
        # Stable local identity prevents each rebuild requiring a new permission entry.
        subprocess.run([
            "codesign", "--force", "--sign", "-", "--requirements",
            f'=designated => identifier "{BUNDLE_ID}"', str(bundle),
        ], check=True)
        subprocess.run(["codesign", "--verify", "--strict", str(bundle)], check=True)
        backup = Path(temp) / "previous.app"
        if output.exists():
            output.rename(backup)
        try:
            bundle.rename(output)
        except OSError:
            if backup.exists():
                backup.rename(output)
            raise
    print(f"Installed: {output}")
    print("Allow DDPM Launcher in System Settings > Privacy & Security > Accessibility.")
    print("Then verify: Command Space > DDPM Launcher > Enter opens Dell's full controls.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.home() / "Applications/DDPM Launcher.app")
    args = parser.parse_args()
    try:
        install(args.output)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"DDPM launcher setup failed: {error}\n")


if __name__ == "__main__":
    main()
