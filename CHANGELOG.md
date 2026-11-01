# Changelog

All notable changes to ChangeScope will be documented here.

## Unreleased

- Established the Python package and CLI interface.
- Added read-only Git change collection, including deleted paths and untracked files.
- Added best-effort handling for deleted Python modules so their importers can still be traced.
- Added best-effort Python import dependency analysis.
- Added reverse dependency traversal and candidate test recommendations.
- Added Markdown and JSON impact reports.
- Added automated tests for Git collection, import analysis, impact traversal, deleted modules, and CLI output.
- Added GitHub Actions CI for Python 3.10–3.13 and Ruff linting.
- Documented static-analysis limitations and safe-by-default behavior.
