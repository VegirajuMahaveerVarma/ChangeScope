from pathlib import Path

from changescope.analyzer import (
    MAX_SOURCE_BYTES,
    build_dependencies,
    discover_python_files,
    module_name,
)


def test_module_name_strips_src_layout(tmp_path: Path) -> None:
    source = tmp_path / "src" / "sample_pkg" / "service.py"
    source.parent.mkdir(parents=True)
    source.touch()
    assert module_name(source, tmp_path) == "sample_pkg.service"


def test_dependency_graph_finds_importers_and_candidate_tests(tmp_path: Path) -> None:
    package = tmp_path / "src" / "sample_pkg"
    tests = tmp_path / "tests"
    package.mkdir(parents=True)
    tests.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "core.py").write_text("def get_value():\n    return 42\n", encoding="utf-8")
    (package / "service.py").write_text(
        "from sample_pkg.core import get_value\n\ndef run():\n    return get_value()\n",
        encoding="utf-8",
    )
    (tests / "test_service.py").write_text(
        "from sample_pkg.service import run\n\ndef test_run():\n    assert run() == 42\n",
        encoding="utf-8",
    )

    module_paths, edges, warnings = build_dependencies(tmp_path)

    assert "sample_pkg.core" in module_paths
    assert any(edge.source == "sample_pkg.service" and edge.target == "sample_pkg.core" for edge in edges)
    assert any(edge.source == "tests.test_service" and edge.target == "sample_pkg.service" for edge in edges)
    assert warnings == []


def test_invalid_python_produces_warning_not_crash(tmp_path: Path) -> None:
    (tmp_path / "broken.py").write_text("def unfinished(:\n", encoding="utf-8")
    _, _, warnings = build_dependencies(tmp_path)
    assert any("Could not parse broken.py" in warning for warning in warnings)


def test_oversized_python_file_is_skipped_with_warning(tmp_path: Path) -> None:
    oversized = tmp_path / "large_module.py"
    oversized.write_bytes(b"#" * (MAX_SOURCE_BYTES + 1))

    module_paths, edges, warnings = build_dependencies(tmp_path)

    assert "large_module" not in module_paths
    assert edges == []
    assert any("large_module.py" in warning and "analysis limit" in warning for warning in warnings)
    assert oversized not in discover_python_files(tmp_path)


def test_oversized_file_warning_does_not_hide_other_modules(tmp_path: Path) -> None:
    (tmp_path / "usable.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "large_module.py").write_bytes(b"#" * (MAX_SOURCE_BYTES + 1))

    module_paths, _, warnings = build_dependencies(tmp_path)

    assert "usable" in module_paths
    assert any("large_module.py" in warning for warning in warnings)


def test_relative_imports_resolve_sibling_and_parent_modules(tmp_path: Path) -> None:
    package = tmp_path / "src" / "sample_pkg"
    nested = package / "subpkg"
    nested.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "shared.py").write_text("VALUE = 1\n", encoding="utf-8")
    (nested / "__init__.py").write_text("from . import sibling\n", encoding="utf-8")
    (nested / "sibling.py").write_text("VALUE = 2\n", encoding="utf-8")
    (nested / "consumer.py").write_text(
        "from ..shared import VALUE\nfrom .sibling import VALUE as OTHER\n",
        encoding="utf-8",
    )

    _, edges, warnings = build_dependencies(tmp_path)
    edge_pairs = {(edge.source, edge.target) for edge in edges}

    assert ("sample_pkg.subpkg", "sample_pkg.subpkg.sibling") in edge_pairs
    assert ("sample_pkg.subpkg.consumer", "sample_pkg.shared") in edge_pairs
    assert ("sample_pkg.subpkg.consumer", "sample_pkg.subpkg.sibling") in edge_pairs
    assert warnings == []


def test_namespace_package_modules_are_discovered_and_connected(tmp_path: Path) -> None:
    namespace = tmp_path / "src" / "namespace_pkg"
    namespace.mkdir(parents=True)
    (namespace / "provider.py").write_text("VALUE = 1\n", encoding="utf-8")
    (namespace / "consumer.py").write_text(
        "from namespace_pkg.provider import VALUE\n", encoding="utf-8"
    )

    module_paths, edges, warnings = build_dependencies(tmp_path)

    assert "namespace_pkg.provider" in module_paths
    assert "namespace_pkg.consumer" in module_paths
    assert any(
        edge.source == "namespace_pkg.consumer" and edge.target == "namespace_pkg.provider"
        for edge in edges
    )
    assert warnings == []
