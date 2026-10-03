#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_raycast_quicklinks.py"
spec = importlib.util.spec_from_file_location("generate_raycast_quicklinks", SCRIPT)
generator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(generator)


class GenerateRaycastQuicklinksTests(unittest.TestCase):
    def make_repo(self, root: Path, name: str) -> Path:
        repository = root / name
        repository.mkdir(parents=True)
        (repository / ".git").mkdir()
        return repository

    def test_roots_come_from_configured_environment_variables(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            personal = root / "personal"
            open_source = root / "open-source"
            personal.mkdir()
            open_source.mkdir()

            with mock.patch.dict(
                os.environ,
                {
                    "PERSONAL_REPOS_DIR": str(personal),
                    "OPEN_SOURCE_REPOS_DIR": str(open_source),
                },
                clear=True,
            ):
                roots = generator.configured_repository_roots()

            self.assertEqual(roots, [personal.resolve(), open_source.resolve()])

    def test_repository_entries_are_deterministic_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            alpha = self.make_repo(root, "alpha")
            zulu = self.make_repo(root, "Zulu")
            (root / "not-a-repo").mkdir()
            self.make_repo(root, ".hidden")

            repositories = generator.find_repositories([root, root])
            entries = generator.build_entries(repositories)

            self.assertEqual(repositories, [alpha.resolve(), zulu.resolve()])
            self.assertEqual(
                entries,
                [
                    {
                        "name": "alpha — VS Code",
                        "link": str(alpha.resolve()),
                        "openWith": "Visual Studio Code",
                    },
                    {
                        "name": "Zulu — VS Code",
                        "link": str(zulu.resolve()),
                        "openWith": "Visual Studio Code",
                    },
                ],
            )

    def test_generated_import_never_overwrites_quicklinks_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raycast_dir = Path(temp_dir) / "raycast"
            raycast_dir.mkdir()
            protected = raycast_dir / "quicklinks.json"
            original = b'[{"name": "keep me"}]\n'
            protected.write_bytes(original)

            with mock.patch.object(generator, "RAYCAST_DIR", raycast_dir):
                with self.assertRaisesRegex(ValueError, "cannot be an output"):
                    generator.write_import(protected, [])
            self.assertEqual(protected.read_bytes(), original)

    def test_write_import_is_stable_when_content_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raycast_dir = Path(temp_dir) / "raycast"
            output = raycast_dir / "repositories-quicklinks.json"
            entries = [
                {
                    "name": "AgentDesk — VS Code",
                    "link": "/tmp/AgentDesk",
                    "openWith": "Visual Studio Code",
                }
            ]

            with mock.patch.object(generator, "RAYCAST_DIR", raycast_dir):
                generator.write_import(output, entries)
                first = output.read_bytes()
                generator.write_import(output, entries)

            self.assertEqual(
                json.loads(first),
                entries,
            )
            self.assertEqual(list(raycast_dir.glob("*.bak.*")), [])


if __name__ == "__main__":
    unittest.main()
