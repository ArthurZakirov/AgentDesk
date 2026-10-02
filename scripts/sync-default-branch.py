#!/usr/bin/env python3
"""Fetch a remote and safely fast-forward its local default branch."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=check
    )


def choose_remote(repo: Path, requested: str | None) -> str:
    remotes = git("remote", cwd=repo).stdout.split()
    if requested:
        if requested not in remotes:
            raise RuntimeError(f"remote {requested!r} does not exist")
        return requested
    if "origin" in remotes:
        return "origin"
    if len(remotes) == 1:
        return remotes[0]
    raise RuntimeError("cannot choose upstream remote; pass --remote")


def remote_default_branch(repo: Path, remote: str) -> str:
    result = git("ls-remote", "--symref", remote, "HEAD", cwd=repo)
    for line in result.stdout.splitlines():
        if line.startswith("ref: refs/heads/") and line.endswith("\tHEAD"):
            return line.removeprefix("ref: refs/heads/").removesuffix("\tHEAD")
    symbolic = git(
        "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote}/HEAD",
        cwd=repo, check=False,
    )
    if symbolic.returncode == 0:
        return symbolic.stdout.strip().removeprefix(f"{remote}/")
    raise RuntimeError(f"cannot determine default branch for {remote}")


def checked_out_worktree(repo: Path, branch: str) -> Path | None:
    current_path: Path | None = None
    for line in git("worktree", "list", "--porcelain", cwd=repo).stdout.splitlines():
        if line.startswith("worktree "):
            current_path = Path(line.removeprefix("worktree "))
        elif line == f"branch refs/heads/{branch}" and current_path:
            return current_path
    return None


def is_clean(worktree: Path) -> bool:
    return not git("status", "--porcelain", cwd=worktree).stdout.strip()


def sync(repo: Path, requested_remote: str | None) -> int:
    repo = Path(git("rev-parse", "--show-toplevel", cwd=repo).stdout.strip())
    remote = choose_remote(repo, requested_remote)
    branch = remote_default_branch(repo, remote)

    git("fetch", "--prune", remote, cwd=repo)
    remote_ref = f"refs/remotes/{remote}/{branch}"
    remote_oid = git("rev-parse", "--verify", remote_ref, cwd=repo).stdout.strip()
    local_ref = f"refs/heads/{branch}"
    local = git("rev-parse", "--verify", local_ref, cwd=repo, check=False)

    if local.returncode != 0:
        git("update-ref", local_ref, remote_oid, "", cwd=repo)
        print(f"created {branch} at {remote}/{branch} ({remote_oid[:12]})")
        return 0

    local_oid = local.stdout.strip()
    if local_oid == remote_oid:
        print(f"{branch} already matches {remote}/{branch} ({remote_oid[:12]})")
        return 0

    ancestor = git("merge-base", "--is-ancestor", local_oid, remote_oid, cwd=repo, check=False)
    if ancestor.returncode != 0:
        print(
            f"SKIP: local {branch} is not a fast-forward of {remote}/{branch}; "
            "preserving local history",
            file=sys.stderr,
        )
        return 2


    worktree = checked_out_worktree(repo, branch)
    if worktree:
        if not is_clean(worktree):
            print(
                f"SKIP: {branch} is checked out with local changes at {worktree}",
                file=sys.stderr,
            )
            return 2
        git("merge", "--ff-only", remote_ref, cwd=worktree)
    else:
        # Compare-and-swap prevents overwriting a ref that changed after our checks.
        git("update-ref", local_ref, remote_oid, local_oid, cwd=repo)

    print(f"fast-forwarded {branch} to {remote}/{branch} ({remote_oid[:12]})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", default=".")
    parser.add_argument("--remote")
    args = parser.parse_args()
    try:
        return sync(Path(args.repository).expanduser().resolve(), args.remote)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        print(f"ERROR: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
