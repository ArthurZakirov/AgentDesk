from __future__ import annotations

from pathlib import Path
import re
import subprocess
import tarfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install-global-guidance.sh"
FIXTURE = ROOT / "tests" / "fixtures" / "agents-md-preview" / "macos"


def make_archive(tmp_path: Path) -> Path:
    archive_root = tmp_path / "AgentDesk-test"
    preview = archive_root / "tests" / "fixtures" / "agents-md-preview" / "macos"
    preview.parent.mkdir(parents=True)
    subprocess.run(["cp", "-R", str(FIXTURE), str(preview)], check=True)
    subprocess.run(["cp", "-R", str(ROOT / "global-guidance"), str(archive_root / "global-guidance")], check=True)
    subprocess.run(["cp", "-R", str(ROOT / "scripts"), str(archive_root / "scripts")], check=True)
    archive = tmp_path / "agentdesk.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(archive_root, arcname=archive_root.name)
    return archive


def run_installer(tmp_path: Path, codex_home: Path) -> subprocess.CompletedProcess[str]:
    archive = make_archive(tmp_path)
    env = {
        "HOME": str(tmp_path / "home"),
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "CODEX_HOME": str(codex_home),
        "AGENTDESK_REPOSITORY": "ArthurZakirov/AgentDesk",
        "AGENTDESK_REF": "test-ref",
        "AGENTDESK_ARCHIVE_URL": archive.as_uri(),
    }
    return subprocess.run([str(SCRIPT)], env=env, text=True, capture_output=True, check=True)


def test_installs_fixture_without_local_checkout(tmp_path: Path) -> None:
    codex_home = tmp_path / ".codex"
    result = run_installer(tmp_path, codex_home)
    rendered = (codex_home / "AGENTS.md").read_text(encoding="utf-8")
    assert "Installed AgentDesk guidance and local sources" in result.stdout
    assert "https://github.com/ArthurZakirov/AgentDesk/blob/test-ref/global-guidance/" not in rendered
    assert "agentdesk-source/global-guidance/" in rendered
    assert f"**AGENTS.md absolute path:** `{codex_home}/AGENTS.md`" in rendered
    assert (codex_home / "agentdesk-source" / "global-guidance" / "agents-md-manifest.yaml").is_file()
    assert (codex_home / "agentdesk-source" / "scripts" / "regenerate-agents-md.py").is_file()
    expected = {path.name for path in (FIXTURE / "agents-md-references").iterdir() if path.is_file()}
    installed = {path.name for path in (codex_home / "agents-md-references").iterdir() if path.is_file()}
    assert installed == expected

    link_pattern = re.compile(r"\[[^\]]+\]\((?:<)?([^)>]+)(?:>)?\)")
    missing: list[str] = []
    for target in link_pattern.findall(rendered):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = target.split("#", 1)[0]
        if path_part and not (codex_home / path_part).resolve().exists():
            missing.append(target)
    assert missing == []


def test_existing_guidance_is_backed_up(tmp_path: Path) -> None:
    codex_home = tmp_path / ".codex"
    refs = codex_home / "agents-md-references"
    refs.mkdir(parents=True)
    (codex_home / "AGENTS.md").write_text("old agents\n", encoding="utf-8")
    (refs / "my-notes.md").write_text("keep me\n", encoding="utf-8")
    old_source = codex_home / "agentdesk-source" / "global-guidance"
    old_source.mkdir(parents=True)
    (old_source / "old.md").write_text("old source\n", encoding="utf-8")
    run_installer(tmp_path, codex_home)
    backups = list((codex_home / "guidance-backups").glob("*/AGENTS.md"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "old agents\n"
    backup_root = backups[0].parent
    assert (backup_root / "agentdesk-source" / "global-guidance" / "old.md").read_text(encoding="utf-8") == "old source\n"
    assert (refs / "my-notes.md").read_text(encoding="utf-8") == "keep me\n"
