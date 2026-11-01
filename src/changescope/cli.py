"""Command-line entry point for ChangeScope."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the initial ChangeScope command-line parser."""
    parser = argparse.ArgumentParser(
        prog="changescope",
        description="Understand the potential impact of your code changes.",
    )
    subparsers = parser.add_subparsers(dest="command")
    analyze = subparsers.add_parser(
        "analyze",
        help="Analyze changed files and their potential impact.",
    )
    analyze.add_argument("--base", help="Base Git revision to compare against.")
    analyze.add_argument("--head", default="HEAD", help="Head Git revision.")
    analyze.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format.",
    )
    analyze.add_argument("--output", help="Write the report to this file.")
    return parser


def main() -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return 0
    parser.error(
        "The analyze command is not implemented yet. "
        "This early-development release only establishes the CLI interface."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
