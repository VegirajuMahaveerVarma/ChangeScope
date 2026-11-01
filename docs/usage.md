# Usage

ChangeScope is an early-stage, read-only analyzer. Its current implementation focuses on Python module import relationships.

## Install for development

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
```

## Analyze working-tree changes

Run inside a Git repository:

```bash
changescope analyze
```

This includes tracked changes compared with `HEAD` and untracked, non-ignored files. Static dependency analysis currently understands Python files only.

## Compare revisions

```bash
changescope analyze --base main --head HEAD
```

The compared revisions determine the changed paths. Analysis reads files currently present in the checked-out working tree, so check out the intended head revision before running the command.

## Export reports

```bash
changescope analyze --format json --output changescope-report.json
changescope analyze --format markdown --output changescope-report.md
```

## Pull request summaries in GitHub Actions

The repository's CI workflow runs ChangeScope on pull requests and appends the Markdown impact report to the GitHub Actions job summary. The workflow compares the pull request with its base branch. This is an advisory report, not a replacement for code review or a full test run.

## Interpret the report

- **Changed files:** paths returned by Git.
- **Potentially affected files:** Python modules that import a changed module, directly or transitively.
- **Dependency evidence:** static import edges used in the analysis.
- **Candidate tests:** affected files that match common Python test naming conventions.
- **Risk indicator:** a simple scope heuristic based on the number of changed and affected files, not a probability of defects.

## Current limitations

- Static import analysis cannot resolve all dynamic imports, reflection, runtime dispatch, or generated code.
- Import relationships do not prove that a particular test exercises a particular behavior.
- Non-Python languages are not analyzed yet.
- The current report does not replace code review, a full test run, or security analysis.
- Analysis is read-only and does not execute tests automatically.
