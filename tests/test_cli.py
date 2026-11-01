from pathlib import Path

from changescope.cli import build_parser, main
from changescope.models import AnalysisResult


def test_cli_exposes_analyze_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["analyze", "--base", "main", "--head", "HEAD"])
    assert args.command == "analyze"
    assert args.base == "main"
    assert args.head == "HEAD"
    assert args.format == "markdown"


def test_cli_help_can_be_built() -> None:
    parser = build_parser()
    assert parser.prog == "changescope"


def test_main_writes_markdown_report(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["changescope", "analyze"])
    monkeypatch.setattr("changescope.cli.repository_root", lambda _: tmp_path)
    monkeypatch.setattr("changescope.cli.changed_paths", lambda *args, **kwargs: ["src/app.py"])
    monkeypatch.setattr(
        "changescope.cli.analyze_changes",
        lambda root, paths: AnalysisResult(root=str(root), changed_files=paths),
    )

    assert main() == 0
    output = capsys.readouterr().out
    assert "# ChangeScope Impact Report" in output
    assert "src/app.py" in output


def test_main_writes_json_report(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["changescope", "analyze", "--format", "json"],
    )
    monkeypatch.setattr("changescope.cli.repository_root", lambda _: tmp_path)
    monkeypatch.setattr("changescope.cli.changed_paths", lambda *args, **kwargs: ["app.py"])
    monkeypatch.setattr(
        "changescope.cli.analyze_changes",
        lambda root, paths: AnalysisResult(root=str(root), changed_files=paths),
    )

    assert main() == 0
    output = capsys.readouterr().out
    assert '"changed_files": [' in output
    assert '"app.py"' in output
