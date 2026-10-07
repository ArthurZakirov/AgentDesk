"""Exercise user-task routing through real Git review aliases."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def test_unreview_from_active_file_directory(tmp_path):
    tasks = json.loads((ROOT / 'config/vscode/tasks.json').read_text())['tasks']
    assert all(task['options']['cwd'] == '${fileDirname}' for task in tasks)
    unreview_task = next(task for task in tasks if task['label'] == 'Git: Unreview')
    source = tmp_path / 'source'
    source.mkdir()
    env = {**os.environ, 'HOME': str(tmp_path), 'GIT_CONFIG_GLOBAL': os.devnull,
           'GIT_CONFIG_NOSYSTEM': '1'}
    bin_dir = tmp_path / 'bin'
    bin_dir.mkdir()
    code = bin_dir / 'code'
    code.write_text('#!/bin/sh\nexit 0\n')
    code.chmod(0o755)
    helper = bin_dir / 'agentdesk-git-review'
    helper.write_bytes((ROOT / 'scripts/git-review-worktree.py').read_bytes())
    helper.chmod(0o755)
    env['PATH'] = str(bin_dir) + os.pathsep + env['PATH']

    def git(*args, cwd=source):
        return subprocess.run(['git', *args], cwd=cwd, env=env,
                              check=True, text=True, capture_output=True).stdout.strip()

    git('init')
    git('config', 'user.name', 'Test')
    git('config', 'user.email', 'test@example.invalid')
    git('config', 'include.path', str(ROOT / 'config/git/gitconfig'))
    (source / 'nested').mkdir()
    file = source / 'nested/file.txt'
    file.write_text('before\n')
    git('add', '.')
    git('commit', '-m', 'base')
    file.write_text('after\n')
    git('commit', '-am', 'target')
    review = Path(git('review', 'HEAD').splitlines()[-1])
    assert (review / 'nested/file.txt').read_text() == 'after\n'
    # VS Code resolves ${fileDirname} from the active review editor, even
    # when the window's original workspace folder is the source checkout.
    result = subprocess.run(unreview_task['command'].split(), cwd=review / 'nested',
                            env=env, check=True, capture_output=True, text=True)
    assert result.stdout.strip() == str(source)
    deadline = time.monotonic() + 5
    while review.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not review.exists()
    assert file.read_text() == 'after\n'
    assert git('status', '--porcelain') == ''
