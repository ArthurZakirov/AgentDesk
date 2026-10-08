from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"

spec = importlib.util.spec_from_file_location("bedtime_guard", SCRIPTS / "bedtime_guard.py")
assert spec and spec.loader
bedtime_guard = importlib.util.module_from_spec(spec)
sys.modules["bedtime_guard"] = bedtime_guard
spec.loader.exec_module(bedtime_guard)

device_spec = importlib.util.spec_from_file_location("device_guard", SCRIPTS / "device_guard.py")
assert device_spec and device_spec.loader
device_guard = importlib.util.module_from_spec(device_spec)
device_spec.loader.exec_module(device_guard)


class WindowTests(unittest.TestCase):
    def test_overnight_boundaries(self) -> None:
        config = {"start": "23:15", "end": "06:45", "timezone": "local"}
        self.assertTrue(bedtime_guard.evaluate(config, "2030-01-01T23:15:00"))
        self.assertTrue(bedtime_guard.evaluate(config, "2030-01-02T06:44:59"))
        self.assertFalse(bedtime_guard.evaluate(config, "2030-01-02T06:45:00"))
        self.assertFalse(bedtime_guard.evaluate(config, "2030-01-01T12:00:00"))

    def test_daytime_window(self) -> None:
        config = {"start": "09:00", "end": "17:00", "timezone": "local"}
        self.assertTrue(bedtime_guard.evaluate(config, "2030-01-01T12:00:00"))
        self.assertFalse(bedtime_guard.evaluate(config, "2030-01-01T18:00:00"))

    def test_warning_only_runs_before_start(self) -> None:
        config = {
            "start": "23:15",
            "end": "06:45",
            "timezone": "local",
            "warning_minutes": 10,
        }
        self.assertTrue(device_guard.warning_due(config, "2030-01-01T23:07:00"))
        self.assertFalse(device_guard.warning_due(config, "2030-01-01T23:16:00"))
        self.assertFalse(device_guard.warning_due(config, "2030-01-02T08:00:00"))

    def test_disabled(self) -> None:
        config = {
            "enabled": False,
            "start": "23:15",
            "end": "06:45",
            "timezone": "local",
        }
        self.assertFalse(bedtime_guard.evaluate(config, "2030-01-01T23:00:00"))


class HookProcessTests(unittest.TestCase):
    def run_hook(self, config: dict[str, object], now: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "bedtime_guard.py"),
                    "--config",
                    str(config_path),
                    "--now",
                    now,
                ],
                input='{"hook_event_name":"UserPromptSubmit","prompt":"private"}',
                capture_output=True,
                text=True,
                check=False,
            )

    def test_block_output_matches_codex_contract(self) -> None:
        result = self.run_hook(
            {"start": "23:15", "end": "06:45", "timezone": "local"},
            "2030-01-01T23:30:00",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["decision"], "block")
        self.assertTrue(json.loads(result.stdout)["reason"])
        self.assertNotIn("private", result.stdout)

    def test_allowed_output_is_empty(self) -> None:
        result = self.run_hook(
            {"start": "23:15", "end": "06:45", "timezone": "local"},
            "2030-01-01T12:00:00",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


class InstallerTests(unittest.TestCase):
    def run_installer(self, home: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "install_guard.py"),
                "--codex-home",
                str(home),
                *arguments,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_install_is_idempotent_and_preserves_other_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original = {
                "custom": {"keep": True},
                "hooks": {
                    "SessionStart": [{"hooks": [{"type": "command", "command": "existing"}]}],
                    "UserPromptSubmit": [
                        {"matcher": "", "hooks": [{"type": "command", "command": "other"}]}
                    ],
                },
            }
            (home / "hooks.json").write_text(json.dumps(original), encoding="utf-8")

            for _ in range(2):
                result = self.run_installer(
                    home,
                    "install",
                    "--start",
                    "23:15",
                    "--end",
                    "06:45",
                    "--timezone",
                    "local",
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            installed = json.loads((home / "hooks.json").read_text(encoding="utf-8"))
            self.assertEqual(installed["custom"], original["custom"])
            self.assertEqual(installed["hooks"]["SessionStart"], original["hooks"]["SessionStart"])
            handlers = [
                handler
                for group in installed["hooks"]["UserPromptSubmit"]
                for handler in group["hooks"]
            ]
            self.assertEqual(
                sum("agentdesk-bedtime-device-guard" in h.get("command", "") for h in handlers),
                1,
            )
            self.assertTrue(any(h.get("command") == "other" for h in handlers))
            self.assertEqual(
                json.loads(
                    (home / "hooks-json" / "bedtime-device-guard" / "config.json").read_text(encoding="utf-8")
                )["start"],
                "23:15",
            )

            verify = self.run_installer(home, "verify")
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_uninstall_preserves_unrelated_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            install_result = self.run_installer(
                home,
                "install",
                "--start",
                "23:15",
                "--end",
                "06:45",
            )
            self.assertEqual(install_result.returncode, 0, install_result.stderr)
            document = json.loads((home / "hooks.json").read_text(encoding="utf-8"))
            document["other"] = "preserved"
            document["hooks"]["Stop"] = [{"hooks": [{"type": "command", "command": "other"}]}]
            (home / "hooks.json").write_text(json.dumps(document), encoding="utf-8")

            result = self.run_installer(home, "uninstall")
            self.assertEqual(result.returncode, 0, result.stderr)
            remaining = json.loads((home / "hooks.json").read_text(encoding="utf-8"))
            self.assertEqual(remaining["other"], "preserved")
            self.assertIn("Stop", remaining["hooks"])
            self.assertNotIn("UserPromptSubmit", remaining["hooks"])
            self.assertFalse((home / "hooks-json" / "bedtime-device-guard").exists())

    def test_invalid_existing_json_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            hooks = home / "hooks.json"
            hooks.write_text("not json", encoding="utf-8")
            result = self.run_installer(
                home,
                "install",
                "--start",
                "23:15",
                "--end",
                "06:45",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(hooks.read_text(encoding="utf-8"), "not json")


if __name__ == "__main__":
    unittest.main()
