"""Exercise preservation, preflight, imports and idempotency on either OS."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("bootstrap", SCRIPTS / "bootstrap-agents-md.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class BootstrapTests(unittest.TestCase):
    def test_preserves_and_installs(self):
        with tempfile.TemporaryDirectory(prefix="guidance-") as tmp:
            root = Path(tmp)
            source = root / "source.md"
            source.write_text("shared preferences\n")
            codex, claude = root / "codex", root / "claude"
            claude.mkdir()
            old = claude / "CLAUDE.md"
            old.write_text("existing preferences\n")
            with self.assertRaises(ValueError):
                bootstrap.install(source, codex, claude)
            self.assertFalse((codex / "AGENTS.md").exists())
            bootstrap.install(source, codex, claude, replace=True, dry_run=True)
            self.assertEqual(old.read_text(), "existing preferences\n")
            bootstrap.install(source, codex, claude, replace=True)
            self.assertEqual(old.read_text(), f"@{source.resolve().as_posix()}\n")
            backups = list(claude.glob("guidance-backups/*/CLAUDE.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "existing preferences\n")
            bootstrap.install(source, codex, claude)
            self.assertEqual(len(list(claude.glob("guidance-backups/*/CLAUDE.md"))), 1)
            opencode = root / "opencode"
            opencode.mkdir()
            config = opencode / "opencode.json"
            config.write_text(json.dumps({"theme": "existing", "instructions": ["other.md"]}))
            bootstrap.install(source, codex, claude, replace=True, opencode_home=opencode)
            data = json.loads(config.read_text())
            self.assertEqual(data["theme"], "existing")
            self.assertEqual(data["instructions"], ["other.md", source.resolve().as_posix()])
            bootstrap.install(source, codex, claude, opencode_home=opencode)
            (codex / "AGENTS.override.md").write_text("override")
            with self.assertRaises(ValueError):
                bootstrap.install(source, codex, claude)

    def test_paths_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="guidance space ") as tmp:
            root = Path(tmp)
            source = root / "private context" / "AGENTS.md"
            source.parent.mkdir()
            source.write_text("shared preferences\n")
            codex = root / "codex home"
            claude = root / "claude home"
            opencode = root / "opencode home"
            bootstrap.install(source, codex, claude, opencode_home=opencode)
            self.assertEqual((claude / "CLAUDE.md").read_text(), f"@{source.resolve().as_posix()}\n")
            self.assertEqual((codex / "AGENTS.md").resolve(), source.resolve())
            self.assertIn(source.resolve().as_posix(), json.loads((opencode / "opencode.json").read_text())["instructions"])

    def test_manifest_guidance_is_atomic_preserving_and_ordered(self):
        with tempfile.TemporaryDirectory(prefix="layered guidance ") as tmp:
            root = Path(tmp)
            guidance = root / "private context"
            components = guidance / "agents-md-components"
            components.mkdir(parents=True)
            first = components / "z-first.md"
            second = components / "a-second.md"
            first.write_text("# First\n\nshared rule one\n")
            second.write_text("# Second\n\nshared rule two\n")
            manifest = guidance / "agents-md-manifest.yaml"
            manifest.write_text(
                "version: 2\n"
                "components:\n"
                "  - path: agents-md-components/z-first.md\n"
                "    children:\n"
                "      - path: agents-md-components/a-second.md\n"
            )
            agents = guidance / "agents-md-references"
            agents.mkdir()
            (agents / "chatgpt-chat.md").write_text("# Chat mode\n\nchat-only rule\n")
            (agents / "repositories.json").write_text('{"version": 1}\n')
            codex, claude, opencode = root / "codex", root / "claude", root / "opencode"
            codex.mkdir()
            old = codex / "AGENTS.md"
            old.write_text("useful local rule\n")
            with self.assertRaises(ValueError):
                bootstrap.install_layered(manifest, codex, claude)
            bootstrap.install_layered(manifest, codex, claude,
                                      replace=True, opencode_home=opencode)
            rendered = old.read_text()
            self.assertTrue(rendered.startswith(bootstrap.GENERATED_MARKER))
            self.assertIn("[AGENTS.md manifest](<../private context/agents-md-manifest.yaml>)", rendered)
            first_marker = "1. [z-first.md](<../private context/agents-md-components/z-first.md>)"
            second_marker = "2. [a-second.md](<../private context/agents-md-components/a-second.md>)"
            self.assertIn(first_marker, rendered)
            self.assertIn(second_marker, rendered)
            self.assertLess(rendered.index(first_marker), rendered.index(second_marker))
            self.assertIn("[`regenerate-agents-md.py`](<", rendered)
            runtime_file = codex / "agents-md-references" / "chatgpt-chat.md"
            self.assertTrue(runtime_file.read_text().startswith(bootstrap.RUNTIME_AGENT_MARKER))
            self.assertIn("chat-only rule", runtime_file.read_text())
            self.assertEqual((codex / "agents-md-references" / "repositories.json").read_text(), '{"version": 1}\n')
            foreign = codex / "agents-md-references" / "my-notes.md"
            foreign.write_text("keep me\n")
            self.assertIn(f"**AGENTS.md absolute path:** `{(codex.resolve() / 'AGENTS.md').as_posix()}`", rendered)
            self.assertIn("Resolving a relative Markdown link or relative path", rendered)
            self.assertIn("directory containing this `AGENTS.md` (`./AGENTS.md`)", rendered)
            self.assertIn("never relative to the active working directory", rendered)
            self.assertIn("## 🗂️ Contents", rendered)
            self.assertIn("- [First](#first)", rendered)
            self.assertIn("  - [Second](#second)", rendered)
            self.assertIn("## 🗂️ Contents\n\n- [Second](#second)", rendered)
            self.assertLess(rendered.index("## 🗂️ Contents\n\n- [Second](#second)"), rendered.index("## Second"))
            self.assertIn("## Second", rendered)
            self.assertNotIn("Global guidance component:", rendered)
            legacy = codex / "AGENTS.md"
            legacy.write_text("<!-- Generated by SkillPort bootstrap-agent-guidance.py. Do not edit. -->\nlegacy\n", encoding="utf-8")
            bootstrap.install_layered(manifest, codex, claude,
                                      opencode_home=opencode)
            self.assertTrue(legacy.read_text(encoding="utf-8").startswith(bootstrap.GENERATED_MARKER))
            self.assertIn("shared rule one", rendered)
            self.assertIn("shared rule two", rendered)
            self.assertEqual(len(list(codex.glob("guidance-backups/*/AGENTS.md"))), 1)
            self.assertEqual(foreign.read_text(), "keep me\n")
            self.assertEqual(list(codex.glob("guidance-backups/*/AGENTS.md"))[0].read_text(), "useful local rule\n")
            expected_imports = f"@{first.resolve().as_posix()}\n@{second.resolve().as_posix()}\n"
            self.assertEqual((claude / "CLAUDE.md").read_text(), expected_imports)
            self.assertEqual(json.loads((opencode / "opencode.json").read_text())["instructions"],
                             [first.resolve().as_posix(), second.resolve().as_posix()])
            first.write_text("# First\n\nupdated shared rule\n")
            bootstrap.install_layered(manifest, codex, claude,
                                      opencode_home=opencode)
            self.assertIn("updated shared rule", old.read_text())
            self.assertEqual(len(list(codex.glob("guidance-backups/*/AGENTS.md"))), 1)


if __name__ == "__main__":
    unittest.main()
