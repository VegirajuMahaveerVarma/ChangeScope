# ChangeScope

[![CI](https://github.com/VegirajuMahaveerVarma/ChangeScope/actions/workflows/ci.yml/badge.svg)](https://github.com/VegirajuMahaveerVarma/ChangeScope/actions/workflows/ci.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**Understand the impact of every code change.**

ChangeScope is a local-first developer tool that analyzes Git changes, traces code relationships, and identifies tests that may be relevant to a change. It helps developers review changes with better context instead of relying on guesswork.

> **Status:** Early development — Python-first MVP

## The problem

A small code change can affect other modules, functions, and tests. In unfamiliar or large repositories, developers may run an unnecessarily large test suite or overlook tests connected to the changed code.

ChangeScope aims to make those relationships visible and produce an evidence-backed impact report.

## What ChangeScope aims to do

- Inspect changes between Git revisions or the working tree.
- Identify changed Python files and module-level import relationships.
- Build a repository-level dependency graph.
- Trace potentially affected modules and tests.
- Recommend candidate tests with an explanation of each recommendation.
- Export reports in Markdown and JSON.
- Integrate with CI after the local workflow is reliable.

ChangeScope reports **potential impact**, not guaranteed breakage. Its output should explain the evidence and limitations behind each result.

## Design principles

- **Local-first:** repository analysis runs on the developer's machine.
- **Deterministic core:** the main analysis does not require an AI service or paid API.
- **Evidence over guesses:** recommendations include the relationships that produced them.
- **Safe by default:** analysis does not modify source files or execute repository commands automatically.
- **Extensible:** language analyzers and test adapters can be added independently.

## Planned MVP

1. Read changed paths from Git.
2. Parse Python source using the standard-library AST.
3. Extract static Python import relationships.
4. Build a directed dependency graph.
5. Trace potential downstream impact from changed modules.
6. Produce a Markdown impact report.
7. Add automated tests and continuous integration.

Test selection will be introduced incrementally. Initial recommendations will be explicitly labeled as candidates, and will not claim complete coverage.

## Example (planned CLI)

```bash
changescope analyze
changescope analyze --base main --head HEAD
changescope analyze --format json --output changescope-report.json
```

The CLI is in early development. The commands are implemented, but analysis currently focuses on static Python imports and module-level dependencies.

## Architecture

```text
Git changes
    |
    v
Change collector
    |
    v
Language analyzers (Python first)
    |
    v
Dependency graph
    |
    v
Impact analysis
    |
    v
Evidence-backed report (Markdown / JSON)
```

See [docs/architecture.md](docs/architecture.md) for the design, [docs/usage.md](docs/usage.md) for detailed commands and report interpretation, and [docs/roadmap.md](docs/roadmap.md) for planned milestones.

## Development

Requirements: Python 3.10 or newer and Git.

```bash
git clone https://github.com/VegirajuMahaveerVarma/ChangeScope.git
cd ChangeScope
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`. On macOS/Linux, use `source .venv/bin/activate`.

## Contributing

Contributions are welcome as the initial interfaces take shape. Read [CONTRIBUTING.md](CONTRIBUTING.md), check the issue tracker, and discuss substantial changes before opening a pull request.

## Project status

ChangeScope is experimental. APIs, report formats, and CLI behavior are not yet stable. Treat recommendations as advisory until validated against your repository and test suite.

## License

GPL-3.0-only. See [LICENSE](LICENSE).
