# Contributing to ChangeScope

Thank you for considering a contribution.

ChangeScope is in early development. The best contributions are focused, tested, documented, and consistent with the project's local-first and evidence-based design.

## Before starting

1. Read the README and architecture notes.
2. Search existing issues and pull requests.
3. For substantial work, open an issue to discuss the proposed approach.
4. Wait for agreement before spending time on a large change.

## Development setup

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
```

## Pull request expectations

- Keep pull requests focused.
- Add or update tests for behavior changes.
- Update documentation when behavior or interfaces change.
- Explain the problem, approach, and validation performed.
- Do not include unrelated formatting or generated files.
- Never include secrets, credentials, or private repository data in fixtures.

## Good first contributions

- Add tests for CLI argument handling.
- Add representative Python parser fixtures.
- Improve handling of syntax errors and unreadable files.
- Document static-analysis limitations.
- Improve Markdown report formatting after the report interface is established.

## Design expectations

- Core analysis must not require network access.
- Avoid paid service dependencies.
- Never execute analyzed repository code automatically.
- Make uncertainty and evidence visible.
- Keep new dependencies justified and optional when practical.

By submitting a contribution, you agree that it may be distributed under the project's GPL-3.0-only license.
