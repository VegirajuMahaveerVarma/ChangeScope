from pathlib import Path

from changescope.impact import analyze_changes
from changescope.report import render_json, render_markdown


def _create_project(root: Path) -> None:
    package = root / "src" / "sample_pkg"
    tests = root / "tests"
    package.mkdir(parents=True)
    tests.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "core.py").write_text("def value():\n    return 1\n", encoding="utf-8")
    (package / "service.py").write_text(
        "from sample_pkg.core import value\n\ndef get():\n    return value()\n",
        encoding="utf-8",
    )
    (tests / "test_service.py").write_text(
        "from sample_pkg.service import get\n\ndef test_get():\n    assert get() == 1\n",
        encoding="utf-8",
    )


def test_impact_analysis_traces_dependents_and_selects_tests(tmp_path: Path) -> None:
    _create_project(tmp_path)
    result = analyze_changes(tmp_path, ["src/sample_pkg/core.py"])

    assert result.changed_files == ["src/sample_pkg/core.py"]
    assert "src/sample_pkg/service.py" in result.affected_files
    assert "tests/test_service.py" in result.recommended_tests
    assert result.dependencies
    assert result.risk in {"low", "medium", "high"}
    assert "potential impact" in render_markdown(result).lower()
    assert render_json(result).startswith("{")


def test_deleted_module_still_impacts_importers(tmp_path: Path) -> None:
    _create_project(tmp_path)
    (tmp_path / "src" / "sample_pkg" / "core.py").unlink()

    result = analyze_changes(tmp_path, ["src/sample_pkg/core.py"])

    assert "src/sample_pkg/service.py" in result.affected_files
    assert "tests/test_service.py" in result.recommended_tests
