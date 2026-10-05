import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "setup-repository-workspace.py"


def run_setup(home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--home", str(home), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_setup_creates_layout_migrates_legacy_and_updates_configs(tmp_path: Path) -> None:
    home = tmp_path / "home"
    legacy_repo = home / "Repos" / "open-source" / "rendercv"
    third_party_existing = home / "Repos" / "third-party" / "existing"
    legacy_repo.mkdir(parents=True)
    third_party_existing.mkdir(parents=True)
    (legacy_repo / "marker.txt").write_text("legacy")
    (home / ".codex").mkdir(parents=True)

    (home / ".zshrc").write_text(
        'export REPOS_DIR="$HOME/Repos"\n'
        'export PERSONAL_REPOS_DIR="$REPOS_DIR/personal"\n'
        'export OPEN_SOURCE_REPOS_DIR="$REPOS_DIR/open-source"\n'
        'alias ll="ls -la"\n'
    )
    (home / ".codex" / "config.toml").write_text(
        'model = "example"\n\n'
        '[shell_environment_policy.set]\n'
        'UNRELATED = "keep"\n'
        'OPEN_SOURCE_REPOS_DIR = "/old/open-source"\n\n'
        '[features]\n'
        'hooks = true\n'
    )

    result = run_setup(home)
    assert result.returncode == 0, result.stderr

    assert not (home / "Repos" / "open-source").exists()
    assert (home / "Repos" / "third-party" / "rendercv" / "marker.txt").read_text() == "legacy"
    assert (home / "Repos" / "personal").is_dir()
    assert (home / "Repos" / "professional").is_dir()
    assert (home / "Tickets").is_dir()

    zshrc = (home / ".zshrc").read_text()
    assert 'alias ll="ls -la"' in zshrc
    assert 'export THIRD_PARTY_REPOS_DIR="$REPOS_DIR/third-party"' in zshrc
    assert 'export PROFESSIONAL_REPOS_DIR="$REPOS_DIR/professional"' in zshrc
    assert 'export TICKETS_DIR="$HOME/Tickets"' in zshrc
    assert "OPEN_SOURCE_REPOS_DIR" not in zshrc

    codex = (home / ".codex" / "config.toml").read_text()
    assert 'UNRELATED = "keep"' in codex
    assert '[features]\nhooks = true' in codex
    assert f'THIRD_PARTY_REPOS_DIR = "{home / "Repos" / "third-party"}"' in codex
    assert f'PROFESSIONAL_REPOS_DIR = "{home / "Repos" / "professional"}"' in codex
    assert f'TICKETS_DIR = "{home / "Tickets"}"' in codex
    assert "OPEN_SOURCE_REPOS_DIR" not in codex

    check = run_setup(home, "--check")
    assert check.returncode == 0, check.stderr


def test_setup_refuses_legacy_merge_when_repo_name_collides(tmp_path: Path) -> None:
    home = tmp_path / "home"
    legacy_repo = home / "Repos" / "open-source" / "same"
    target_repo = home / "Repos" / "third-party" / "same"
    legacy_repo.mkdir(parents=True)
    target_repo.mkdir(parents=True)
    (legacy_repo / "legacy.txt").write_text("legacy")
    (target_repo / "target.txt").write_text("target")

    result = run_setup(home)

    assert result.returncode != 0
    assert (legacy_repo / "legacy.txt").exists()
    assert (target_repo / "target.txt").exists()
