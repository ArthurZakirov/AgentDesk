from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "agents-md-preview" / "macos"
spec = importlib.util.spec_from_file_location("bootstrap", SCRIPTS / "bootstrap-agents-md.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


def generate_preview(destination: Path) -> None:
    bootstrap.install_layered(
        ROOT / "global-guidance" / "agents-md-manifest.yaml",
        destination,
        destination / ".claude-unused",
        replace=True,
        opencode_home=None,
        agents_path_label="<preview>/AGENTS.md",
    )


def file_map(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".claude-unused" not in path.parts
    }


def test_agents_md_preview_matches_generated_output() -> None:
    with tempfile.TemporaryDirectory(dir=ROOT / "tests" / "fixtures") as tmp:
        generated = Path(tmp) / "macos"
        generate_preview(generated)
        assert file_map(generated) == file_map(FIXTURE)


def test_agents_md_preview_relative_links_resolve() -> None:
    markdown_files = [FIXTURE / "AGENTS.md", *sorted((FIXTURE / "agents-md-references").glob("*.md"))]
    pattern = re.compile(r"\[[^\]]+\]\((?:<)?([^)>]+)(?:>)?\)")
    missing: list[str] = []
    for markdown in markdown_files:
        for target in pattern.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (markdown.parent / path_part).resolve()
            if not resolved.exists():
                missing.append(f"{markdown.relative_to(FIXTURE)} -> {target}")
    assert missing == []


def test_agents_md_preview_exposes_grouped_navigation() -> None:
    rendered = (FIXTURE / "AGENTS.md").read_text(encoding="utf-8")
    assert "- [🛠️ Workspace and agent system](#workspace-and-agent-system)" in rendered
    assert "  - [🛠️ Updating this AGENTS.md](#agents-md-maintenance)" in rendered
    assert "- [🎛️ Runtime and interaction](#runtime-and-interaction)" in rendered
    assert "- [🧭 Reasoning and agent behavior](#reasoning-and-agent-behavior)" in rendered
    assert "- [🧠 Information presentation](#information-presentation)" in rendered
    assert "Global guidance component:" not in rendered
    assert sum(line == "---" for line in rendered.splitlines()) == 4
    assert sum(line == "<br><br>" for line in rendered.splitlines()) == 4
