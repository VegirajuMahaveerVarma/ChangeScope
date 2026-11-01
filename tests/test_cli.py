from changescope.cli import build_parser


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
