# Roadmap

This roadmap is directional. Checkboxes reflect implementation and tests in the repository, not independent release certification.

## 0.1 — Local Python MVP

- [x] Define the project purpose and design principles.
- [x] Establish the Python package layout and CLI.
- [x] Collect working-tree changes and compare Git revisions.
- [x] Parse Python files using the standard-library AST.
- [x] Build module-level import dependency edges.
- [x] Trace reverse dependencies from changed modules.
- [x] Generate Markdown and JSON impact reports.
- [x] Recommend candidate tests from static import relationships.
- [x] Add unit tests and GitHub Actions CI.
- [x] Document limitations, safety boundaries, and usage.
- [ ] Verify behavior against several real-world repositories and publish a tagged alpha release.

## 0.2 — Improve analysis quality

- [x] Add a representative Python repository fixture and expected impact snapshot.
- [x] Improve regression coverage for relative imports and namespace-package modules.
- [x] Warn when source files exceed the analysis limit or cannot be inspected.
- [ ] Improve test discovery and document false-positive/false-negative cases.
- [ ] Add coverage-data import as optional evidence.
- [ ] Benchmark performance on small, medium, and large repositories.

## 0.3 — Developer workflow integration

- [x] Add GitHub Actions summary output for pull requests.
- [ ] Add optional pull-request annotations.
- [ ] Add TypeScript analyzer as an independent extension.
- [ ] Add graph visualization as an optional report format.
- [ ] Gather feedback from external users and contributors.

## 1.0 — Stability

- [ ] Stabilize public APIs and report schema.
- [ ] Define supported Python constructs and compatibility guarantees.
- [ ] Establish security reporting and release procedures.
- [ ] Publish complete documentation and a tested package release.
