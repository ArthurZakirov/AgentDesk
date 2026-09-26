#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "regenerate-agents-md.py"


class RegenerateAgentsMdTests(unittest.TestCase):
    def test_argumentless_contract_with_explicit_test_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            agentdesk = root / "AgentDesk"
            guidance = agentdesk / "global-guidance"
            guidance.mkdir(parents=True)
            (guidance / "common.md").write_text("common rule\n", encoding="utf-8")
            (guidance / "macos.md").write_text("mac rule\n", encoding="utf-8")
            codex = root / ".codex"
            claude = root / ".claude"
            opencode = root / ".config" / "opencode"

            fake_scripts = agentdesk / "scripts"
            fake_scripts.mkdir(parents=True)
            for name in ("regenerate-agents-md.py", "bootstrap-agents-md.py", "repository_registry.py"):
                (fake_scripts / name).write_text((ROOT / "scripts" / name).read_text(encoding="utf-8"), encoding="utf-8")

            subprocess.run([
                sys.executable, str(fake_scripts / "regenerate-agents-md.py"),
                "--platform", "macos",
                "--codex-home", str(codex),
                "--claude-home", str(claude),
                "--opencode-home", str(opencode),
            ], check=True)

            rendered = (codex / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("common rule", rendered)
            self.assertIn("mac rule", rendered)
            self.assertIn("bootstrap-agents-md.py", rendered)


if __name__ == "__main__":
    unittest.main()
