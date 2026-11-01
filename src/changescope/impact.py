"""Change impact traversal and candidate test selection."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from changescope.analyzer import build_dependencies, module_name
from changescope.models import AnalysisResult


def _is_test(path: str) -> bool:
    """Return whether a Python path follows common pytest test-file naming."""
    candidate = Path(path)
    return candidate.suffix == ".py" and (
        candidate.name.startswith("test_") or candidate.name.endswith("_test.py")
    )


def _risk(changed_count: int, affected_count: int, warnings: int) -> str:
    if not changed_count:
        return "unknown"
    score = changed_count + affected_count + int(bool(warnings))
    if score >= 15:
        return "high"
    if score >= 6:
        return "medium"
    return "low"


def analyze_changes(root: Path, changed_files: list[str]) -> AnalysisResult:
    """Analyze changed files and trace potential reverse dependency impact."""
    root = root.resolve()
    changed_set = set(changed_files)
    extra_modules = {
        name
        for path in changed_set
        if (name := module_name(root / path, root)) is not None
    }
    module_paths, dependencies, warnings = build_dependencies(root, extra_modules)
    path_to_module = {
        path.relative_to(root).as_posix(): name for name, path in module_paths.items()
    }
    changed_modules = {
        path_to_module.get(path) or module_name(root / path, root)
        for path in changed_set
    }
    changed_modules.discard(None)

    reverse: dict[str, set[str]] = {}
    for edge in dependencies:
        reverse.setdefault(edge.target, set()).add(edge.source)

    impacted_modules: set[str] = set()
    queue = deque(sorted(changed_modules))
    visited = set(changed_modules)
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse.get(current, set())):
            if dependent in visited:
                continue
            visited.add(dependent)
            impacted_modules.add(dependent)
            queue.append(dependent)

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

    relevant_modules = changed_modules | impacted_modules
    relevant_dependencies = [
        edge
        for edge in dependencies
        if edge.source in relevant_modules and edge.target in relevant_modules
    ]

    return AnalysisResult(
        root=str(root),
        changed_files=sorted(changed_set),
        affected_files=affected_files,
        recommended_tests=recommended_tests,
        dependencies=relevant_dependencies,
        warnings=warnings,
        risk=_risk(len(changed_set), len(affected_files), len(warnings)),
    )
