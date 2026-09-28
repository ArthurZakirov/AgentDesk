from __future__ import annotations

from pathlib import Path
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
    assert "Installed AgentDesk guidance" in result.stdout
    assert "https://github.com/ArthurZakirov/AgentDesk/blob/test-ref/global-guidance/" in rendered
    assert f"**AGENTS.md absolute path:** `{codex_home}/AGENTS.md`" in rendered
    expected = {path.name for path in (FIXTURE / "agents-md-references").iterdir() if path.is_file()}
    installed = {path.name for path in (codex_home / "agents-md-references").iterdir() if path.is_file()}
    assert installed == expected


def test_existing_guidance_is_backed_up(tmp_path: Path) -> None:
    codex_home = tmp_path / ".codex"
    refs = codex_home / "agents-md-references"
    refs.mkdir(parents=True)
    (codex_home / "AGENTS.md").write_text("old agents\n", encoding="utf-8")
    (refs / "my-notes.md").write_text("keep me\n", encoding="utf-8")
    run_installer(tmp_path, codex_home)
    backups = list((codex_home / "guidance-backups").glob("*/AGENTS.md"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "old agents\n"
    assert (refs / "my-notes.md").read_text(encoding="utf-8") == "keep me\n"
