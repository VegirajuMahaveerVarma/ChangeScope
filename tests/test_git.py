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


def test_deleted_tracked_file_is_reported(tmp_path: Path) -> None:
    _run_git(tmp_path, "init")
    _run_git(tmp_path, "config", "user.email", "test@example.com")
    _run_git(tmp_path, "config", "user.name", "Test")
    deleted = tmp_path / "deleted.py"
    deleted.write_text("VALUE = 1\n", encoding="utf-8")
    _run_git(tmp_path, "add", "deleted.py")
    _run_git(tmp_path, "commit", "-m", "initial")
    deleted.unlink()

    assert changed_paths(repository_root(tmp_path)) == ["deleted.py"]


def test_revision_comparison_reports_changed_paths(tmp_path: Path) -> None:
    _run_git(tmp_path, "init")
    _run_git(tmp_path, "config", "user.email", "test@example.com")
    _run_git(tmp_path, "config", "user.name", "Test")
    source = tmp_path / "app.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    _run_git(tmp_path, "add", "app.py")
    _run_git(tmp_path, "commit", "-m", "initial")
    base = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    source.write_text("VALUE = 2\n", encoding="utf-8")
    _run_git(tmp_path, "commit", "-am", "update")

    assert changed_paths(repository_root(tmp_path), base=base) == ["app.py"]
