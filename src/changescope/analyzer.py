"""Static Python import analysis using the standard-library AST."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

from changescope.models import Dependency

IGNORED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "site-packages",
    "node_modules", "build", "dist", ".tox", ".pytest_cache",
}
MAX_SOURCE_BYTES = 1_000_000


def module_name(path: Path, root: Path) -> str | None:
    """Convert a Python file path into a best-effort importable module name."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    if relative.suffix != ".py":
        return None
    parts = list(relative.with_suffix("").parts)
    if parts and parts[0] == "src":
        parts.pop(0)
    if parts and parts[-1] == "__init__":
        parts.pop()
    if not parts or any(not part.isidentifier() for part in parts):
        return None
    return ".".join(parts)


def discover_python_files(root: Path) -> list[Path]:
    """Find Python files while excluding common generated/environment folders."""
    found: list[Path] = []
    for path in root.rglob("*.py"):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        try:
            if path.is_file() and path.stat().st_size <= MAX_SOURCE_BYTES:
                found.append(path)
        except OSError:
            continue
    return sorted(found)


def _resolve_from_import(
    node: ast.ImportFrom,
    current_module: str,
    known_modules: set[str],
    is_package: bool = False,
) -> set[str]:
    package = current_module if is_package else current_module.rpartition(".")[0]
    if not package and node.level:
        return set()

    if node.level:
        relative = "." * node.level + (node.module or "")
        try:
            resolved_base = importlib.util.resolve_name(relative, package)
        except (ImportError, ValueError):
            return set()
    elif node.module:
        resolved_base = node.module
    else:
        return set()

    candidates: set[str] = set()
    if resolved_base in known_modules:
        candidates.add(resolved_base)
    for alias in node.names:
        candidate = f"{resolved_base}.{alias.name}"
        if candidate in known_modules:
            candidates.add(candidate)
    return candidates


def build_dependencies(
    root: Path,
    extra_modules: set[str] | None = None,
) -> tuple[dict[str, Path], list[Dependency], list[str]]:
    """Build module import edges, retaining explicitly changed-but-missing modules."""
    module_paths: dict[str, Path] = {}
    warnings: list[str] = []
    for path in discover_python_files(root):
        name = module_name(path, root)
        if name:
            module_paths[name] = path

    known_modules = set(module_paths) | (extra_modules or set())
    dependencies: set[tuple[str, str, str, int | None]] = set()

    for name, path in module_paths.items():
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            warnings.append(f"Could not read {path.relative_to(root)}: {exc}")
            continue
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            location = f" at line {exc.lineno}" if exc.lineno else ""
            warnings.append(
                f"Could not parse {path.relative_to(root)}{location}: {exc.msg}"
            )
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = alias.name
                    if target in known_modules:
                        dependencies.add((name, target, "imports", node.lineno))
                    else:
                        parts = target.split(".")
                        for end in range(len(parts) - 1, 0, -1):
                            candidate = ".".join(parts[:end])
                            if candidate in known_modules:
                                dependencies.add((name, candidate, "imports", node.lineno))
                                break
            elif isinstance(node, ast.ImportFrom):
                for target in _resolve_from_import(
                    node, name, known_modules, is_package=path.name == "__init__.py"
                ):
                    dependencies.add((name, target, "imports", node.lineno))

    edges = [
        Dependency(source=source, target=target, kind=kind, line=line)
        for source, target, kind, line in sorted(
            dependencies, key=lambda item: (item[0], item[1], item[2], item[3] or 0)
        )
    ]
    return module_paths, edges, warnings
