"""Safe, read-only Git helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """Raised when Git cannot provide the requested repository information."""


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitError(f"Could not run Git: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or "Git command failed."
        raise GitError(detail)
    return result.stdout


def repository_root(path: str | Path) -> Path:
    """Resolve the root of a Git working tree."""
    candidate = Path(path).expanduser().resolve()
    if not candidate.exists() or not candidate.is_dir():
        raise GitError(f"Repository path is not a directory: {candidate}")
    output = _git(candidate, "rev-parse", "--show-toplevel").strip()
    return Path(output).resolve()


def changed_paths(
    root: Path,
    base: str | None = None,
    head: str = "HEAD",
) -> list[str]:
    """Return changed paths, including untracked files for working-tree analysis.

    With base specified, compare base to head. Without base, compare the working
    tree and index with HEAD and include untracked, non-ignored files.
    """
    if base:
        output = _git(
            root, "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"
        )
        paths = {line.strip() for line in output.splitlines() if line.strip()}
    else:
        output = _git(root, "diff", "--name-only", "--diff-filter=ACMR", "HEAD")
        paths = {line.strip() for line in output.splitlines() if line.strip()}
        untracked = _git(root, "ls-files", "--others", "--exclude-standard")
        paths.update(line.strip() for line in untracked.splitlines() if line.strip())

    return sorted(path for path in paths if not path.startswith("../"))
