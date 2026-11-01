import subprocess
from pathlib import Path

import pytest

from changescope.git import GitError, changed_paths, repository_root


def _run_git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def test_repository_root_and_untracked_changes(tmp_path: Path) -> None:
    _run_git(tmp_path, "init")
    _run_git(tmp_path, "config", "user.email", "test@example.com")
    _run_git(tmp_path, "config", "user.name", "Test")
    (tmp_path / "tracked.py").write_text("value = 1\n", encoding="utf-8")
    _run_git(tmp_path, "add", "tracked.py")
    _run_git(tmp_path, "commit", "-m", "initial")
    (tmp_path / "tracked.py").write_text("value = 2\n", encoding="utf-8")
    (tmp_path / "new.py").write_text("value = 3\n", encoding="utf-8")

    root = repository_root(tmp_path)
    assert root == tmp_path.resolve()
    assert changed_paths(root) == ["new.py", "tracked.py"]


def test_non_repository_raises_git_error(tmp_path: Path) -> None:
    with pytest.raises(GitError):
        repository_root(tmp_path)
