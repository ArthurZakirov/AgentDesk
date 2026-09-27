#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "chezmoi-guidance-pilot.py"
spec = importlib.util.spec_from_file_location("chezmoi_guidance_pilot", SCRIPT)
pilot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(pilot)


FAKE_CHEZMOI = r'''#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

arguments = sys.argv[1:]
source = Path(arguments[arguments.index("--source") + 1])
destination = Path(arguments[arguments.index("--destination") + 1])
if "--dry-run" not in arguments:
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        parts = list(relative.parts)
        if parts[0].startswith("dot_"):
            parts[0] = "." + parts[0][4:]
        target = destination.joinpath(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
'''


class ChezmoiGuidancePilotTests(unittest.TestCase):
    def make_fake_chezmoi(self, root: Path) -> Path:
        binary = root / "chezmoi"
        binary.write_text(FAKE_CHEZMOI, encoding="utf-8")
        binary.chmod(0o755)
        return binary

    def test_rendered_source_uses_target_home_and_canonical_agentdesk_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            codex_home = home / ".codex"
            source = root / "source"
            source.mkdir()

            pilot.render_source(source, home, codex_home)

            rendered = (source / "dot_codex" / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(str(codex_home / "AGENTS.md"), rendered)
            expected_manifest = Path(pilot.os.path.relpath(pilot.MANIFEST, start=codex_home)).as_posix()
            self.assertIn(expected_manifest, rendered)
            self.assertTrue((source / "dot_codex" / "agents-md-references" / "codex.md").is_file())

    def test_apply_refuses_unmanaged_first_run_without_explicit_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            codex_home = home / ".codex"
            codex_home.mkdir(parents=True)
            (codex_home / "AGENTS.md").write_text("personal rule\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "apply", "--home", str(home),
                 "--chezmoi-bin", str(self.make_fake_chezmoi(root))],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to replace unmanaged guidance", result.stderr)
            self.assertEqual((codex_home / "AGENTS.md").read_text(encoding="utf-8"), "personal rule\n")

    def test_apply_and_rollback_restore_previous_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            codex_home = home / ".codex"
            codex_home.mkdir(parents=True)
            original = "personal rule\n"
            (codex_home / "AGENTS.md").write_text(original, encoding="utf-8")
            references = codex_home / "agents-md-references"
            references.mkdir()
            foreign = references / "my-notes.md"
            foreign.write_text("keep me\n", encoding="utf-8")
            state = root / "state"
            binary = self.make_fake_chezmoi(root)

            subprocess.run(
                [sys.executable, str(SCRIPT), "apply", "--home", str(home),
                 "--state-dir", str(state), "--chezmoi-bin", str(binary), "--replace-existing"],
                check=True,
            )
            self.assertTrue((codex_home / "AGENTS.md").read_text(encoding="utf-8").startswith(pilot.GENERATED_MARKER))
            self.assertTrue((codex_home / "agents-md-references" / "codex.md").exists())

            subprocess.run(
                [sys.executable, str(SCRIPT), "rollback", "--home", str(home), "--state-dir", str(state)],
                check=True,
            )
            self.assertEqual((codex_home / "AGENTS.md").read_text(encoding="utf-8"), original)
            self.assertFalse((codex_home / "agents-md-references" / "codex.md").exists())
            self.assertEqual(foreign.read_text(encoding="utf-8"), "keep me\n")

    def test_codex_home_must_be_one_home_local_directory_on_every_platform(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir) / "home"
            self.assertEqual(pilot.relative_codex_home(home, home / ".codex"), Path(".codex"))
            with self.assertRaisesRegex(ValueError, "direct child"):
                pilot.relative_codex_home(home, home / "nested" / ".codex")
            with self.assertRaisesRegex(ValueError, "inside"):
                pilot.relative_codex_home(home, Path(temp_dir) / "outside")


if __name__ == "__main__":
    unittest.main()
