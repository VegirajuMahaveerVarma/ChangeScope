from pathlib import Path

from changescope.analyzer import build_dependencies, module_name


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
