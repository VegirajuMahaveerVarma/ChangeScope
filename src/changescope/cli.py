"""Command-line interface for ChangeScope."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from changescope.git import GitError, changed_paths, repository_root
from changescope.impact import analyze_changes
from changescope.report import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="changescope",
        description="Understand the potential impact of your code changes.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser(
        "analyze",
        help="Analyze changed files and their potential impact.",
    )
    analyze.add_argument("--root", default=".", help="Git repository path (default: current directory).")
    analyze.add_argument("--base", help="Base revision to compare against.")
    analyze.add_argument("--head", default="HEAD", help="Head revision when --base is supplied.")
    analyze.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format.",
    )
    analyze.add_argument("--output", help="Write the report to a file instead of stdout.")
    return parser


def _analyze(args: argparse.Namespace) -> int:
    try:
        root = repository_root(args.root)
        paths = changed_paths(root, base=args.base, head=args.head)
        result = analyze_changes(root, paths)
        output = render_json(result) if args.format == "json" else render_markdown(result)
        if args.output:
            destination = Path(args.output).expanduser().resolve()
            destination.write_text(output + ("" if output.endswith("\n") else "\n"), encoding="utf-8")
            print(f"ChangeScope report written to {destination}")
        else:
            print(output)
        return 0
    except (GitError, OSError, ValueError) as exc:
        print(f"changescope: error: {exc}", file=sys.stderr)
        return 2


def main() -> int:
    """Run ChangeScope."""
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "analyze":
        return _analyze(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
