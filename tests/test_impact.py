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


def test_representative_fixture_matches_expected_impact_snapshot() -> None:
    fixture_root = Path(__file__).parent / "fixtures" / "impact_project"
    snapshot_path = Path(__file__).parent / "fixtures" / "expected_core_change.md"

    result = analyze_changes(fixture_root, ["src/demo_pkg/core.py"])

    assert result.affected_files == [
        "src/demo_pkg/service.py",
        "tests/helpers.py",
        "tests/test_service.py",
    ]
    assert result.recommended_tests == ["tests/test_service.py"]
    assert "tests/helpers.py" not in result.recommended_tests
    assert render_markdown(result) == snapshot_path.read_text(encoding="utf-8")


def test_suffix_test_naming_is_recommended(tmp_path: Path) -> None:
    _create_project(tmp_path)
    suffix_test = tmp_path / "tests" / "service_test.py"
    suffix_test.write_text(
        "from sample_pkg.service import get\n\ndef checks_get():\n    assert get() == 1\n",
        encoding="utf-8",
    )

    result = analyze_changes(tmp_path, ["src/sample_pkg/core.py"])

    assert "tests/service_test.py" in result.recommended_tests


def test_dependency_cycle_terminates_and_reports_each_file_once(tmp_path: Path) -> None:
    package = tmp_path / "src" / "cycle_pkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "alpha.py").write_text(
        "from cycle_pkg.beta import VALUE\nVALUE = 1\n", encoding="utf-8"
    )
    (package / "beta.py").write_text(
        "from cycle_pkg.alpha import VALUE\nVALUE = 2\n", encoding="utf-8"
    )

    result = analyze_changes(tmp_path, ["src/cycle_pkg/alpha.py"])

    assert result.affected_files == ["src/cycle_pkg/beta.py"]
    assert len(result.affected_files) == len(set(result.affected_files))


def test_non_python_change_includes_scope_warning(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Project\n", encoding="utf-8")

    result = analyze_changes(tmp_path, ["README.md"])

    assert any("No changed files matched" in warning for warning in result.warnings)
