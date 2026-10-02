from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync-default-branch.py"


def run(*args: str, cwd: Path, check: bool = True):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=check)


def git(cwd: Path, *args: str):
    return run("git", *args, cwd=cwd)


def setup_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    remote = tmp_path / "remote.git"
    seed = tmp_path / "seed"
    clone = tmp_path / "clone"
    git(tmp_path, "init", "--bare", str(remote))
    git(tmp_path, "init", "-b", "trunk", str(seed))
    git(seed, "config", "user.email", "test@example.com")
    git(seed, "config", "user.name", "Test")
    (seed / "file.txt").write_text("one\n")
    git(seed, "add", ".")
    git(seed, "commit", "-m", "initial")
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-u", "origin", "trunk")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/trunk")
    git(tmp_path, "clone", str(remote), str(clone))
    git(clone, "config", "user.email", "test@example.com")
    git(clone, "config", "user.name", "Test")
    return remote, seed, clone


def advance(seed: Path, text: str = "two\n") -> str:
    (seed / "file.txt").write_text(text)
    git(seed, "commit", "-am", "advance")
    git(seed, "push")
    return git(seed, "rev-parse", "HEAD").stdout.strip()


def sync(clone: Path):
    return run("python3", str(SCRIPT), str(clone), cwd=clone, check=False)


def test_fast_forwards_default_branch_while_feature_is_checked_out(tmp_path: Path):
    _, seed, clone = setup_repo(tmp_path)
    git(clone, "switch", "-c", "feature")
    expected = advance(seed)
    result = sync(clone)
    assert result.returncode == 0, result.stderr
    assert git(clone, "rev-parse", "trunk").stdout.strip() == expected
    assert git(clone, "branch", "--show-current").stdout.strip() == "feature"


def test_updates_clean_checked_out_default_branch(tmp_path: Path):
    _, seed, clone = setup_repo(tmp_path)
    expected = advance(seed)
    result = sync(clone)
    assert result.returncode == 0, result.stderr
    assert git(clone, "rev-parse", "HEAD").stdout.strip() == expected


def test_preserves_dirty_checked_out_default_branch(tmp_path: Path):
    _, seed, clone = setup_repo(tmp_path)
    before = git(clone, "rev-parse", "trunk").stdout.strip()
    (clone / "local.txt").write_text("dirty\n")
    advance(seed)
    result = sync(clone)
    assert result.returncode == 2
    assert "local changes" in result.stderr
    assert git(clone, "rev-parse", "trunk").stdout.strip() == before
    assert (clone / "local.txt").read_text() == "dirty\n"


def test_preserves_diverged_local_default_branch(tmp_path: Path):
    _, seed, clone = setup_repo(tmp_path)
    git(clone, "switch", "-c", "feature")
    git(clone, "switch", "trunk")
    (clone / "local.txt").write_text("local\n")
    git(clone, "add", ".")
    git(clone, "commit", "-m", "local")
    local = git(clone, "rev-parse", "trunk").stdout.strip()
    git(clone, "switch", "feature")
    advance(seed)

    result = sync(clone)
    assert result.returncode == 2
    assert "not a fast-forward" in result.stderr
    assert git(clone, "rev-parse", "trunk").stdout.strip() == local


def test_creates_missing_local_default_branch(tmp_path: Path):
    _, seed, clone = setup_repo(tmp_path)
    git(clone, "switch", "--detach")
    git(clone, "branch", "-D", "trunk")
    expected = advance(seed)

    result = sync(clone)
    assert result.returncode == 0, result.stderr
    assert git(clone, "rev-parse", "trunk").stdout.strip() == expected
