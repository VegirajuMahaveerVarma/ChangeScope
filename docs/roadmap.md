# Roadmap

This roadmap is directional. Milestones depend on implementation and user feedback.

## 0.1 — Foundation

- [x] Define the project purpose and design principles.
- [x] Establish the Python package layout.
- [x] Add an initial CLI interface.
- [ ] Collect changed paths from Git safely.
- [ ] Parse Python files using AST.
- [ ] Build a basic module dependency graph.
- [ ] Generate a Markdown impact report.
- [ ] Add unit and integration tests.

## 0.2 — Useful impact analysis

- [ ] Trace reverse dependencies from changed modules.
- [ ] Include file and line evidence in results.
- [ ] Add JSON report output.
- [ ] Add fixtures from representative Python repositories.
- [ ] Document known limitations and false positives.

## 0.3 — Test impact recommendations

- [ ] Discover test files using configurable patterns.
- [ ] Associate tests with source modules using static evidence.
- [ ] Optionally import coverage data.
- [ ] Rank candidate tests transparently.
- [ ] Compare recommendations with full-suite test runs.

## 0.4 — Contributor and CI experience

- [ ] Add GitHub Actions integration.
- [ ] Publish machine-readable CI summaries.
- [ ] Add TypeScript analyzer as an independent extension.
- [ ] Improve performance on larger repositories.
- [ ] Gather feedback from external users.

## 1.0 — Stability

- [ ] Stabilize public APIs and report schema.
- [ ] Define supported Python constructs and limitations.
- [ ] Establish compatibility and security policies.
- [ ] Publish documentation and release process.
