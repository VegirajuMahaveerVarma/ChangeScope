"""Change impact traversal and candidate test selection."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from changescope.analyzer import build_dependencies, module_name
from changescope.models import AnalysisResult, Dependency


def _is_test(path: str) -> bool:
    candidate = Path(path)
    return (
        candidate.name.startswith("test_")
        or candidate.name.endswith("_test.py")
        or "tests" in candidate.parts
    )


def _risk(changed_count: int, affected_count: int, warnings: int) -> str:
    if not changed_count:
        return "unknown"
    score = changed_count + affected_count
    if warnings:
        score += 1
    if score >= 15:
        return "high"
    if score >= 6:
        return "medium"
    return "low"


def analyze_changes(
    root: Path,
    changed_files: list[str],
) -> AnalysisResult:
    """Analyze changed files and trace potential reverse dependency impact."""
    module_paths, dependencies, warnings = build_dependencies(root)
    path_to_module = {
        path.relative_to(root).as_posix(): name for name, path in module_paths.items()
    }
    changed_modules = {
        path_to_module[path]
        for path in changed_files
        if path in path_to_module
    }

    reverse: dict[str, set[str]] = {}
    for edge in dependencies:
        reverse.setdefault(edge.target, set()).add(edge.source)

    impacted_modules: set[str] = set()
    queue = deque(changed_modules)
    visited = set(changed_modules)
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse.get(current, set())):
            if dependent in visited:
                continue
            visited.add(dependent)
            impacted_modules.add(dependent)
            queue.append(dependent)

    changed_set = set(changed_files)
    affected_files = sorted(
        {
            module_paths[name].relative_to(root).as_posix()
            for name in impacted_modules
            if name in module_paths
        }
        - changed_set
    )
    recommended_tests = sorted(path for path in affected_files if _is_test(path))

    if not changed_modules and changed_files:
        warnings.append(
            "No changed files matched a statically recognized Python module. "
            "Non-Python files and non-import relationships are not analyzed yet."
        )

    return AnalysisResult(
        root=str(root),
        changed_files=sorted(set(changed_files)),
        affected_files=affected_files,
        recommended_tests=recommended_tests,
        dependencies=dependencies,
        warnings=warnings,
        risk=_risk(len(changed_files), len(affected_files), len(warnings)),
    )
