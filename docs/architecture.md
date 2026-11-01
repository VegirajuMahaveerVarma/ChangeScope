# Architecture

## Goal

Keep ChangeScope's analysis deterministic, local, testable, and independent of optional integrations.

## Initial pipeline

1. **Change collector:** obtains changed paths and revision metadata from Git.
2. **Language analyzer:** parses supported files and extracts definitions and relationships.
3. **Graph builder:** stores module and symbol relationships in a directed graph.
4. **Impact engine:** traverses reverse relationships from changed nodes to find possible downstream effects.
5. **Test mapper:** associates tests with source nodes using evidence such as imports, references, and optional coverage data.
6. **Reporter:** emits a stable structured result and renders Markdown or JSON.

## Initial Python analyzer

Use Python's standard-library AST module first. Extract module imports, top-level definitions, classes, and function definitions. Preserve file and line locations so reports can point to evidence.

Do not claim complete call-graph accuracy. Dynamic imports, reflection, runtime dispatch, generated code, and unresolved imports limit static analysis.

## Graph direction

Represent an edge from A to B as “A depends on B.” For a changed node B, traverse reverse edges to discover nodes that may depend on B.

Keep edge types explicit, for example `imports`, `references`, and later `covered_by_test`.

## Safety

- Do not execute code from the analyzed repository.
- Do not automatically run test commands discovered in project files.
- Do not modify the working tree.
- Treat repository contents as untrusted input.
- Bound file sizes and handle syntax errors without stopping the entire analysis.

## Future extension points

Language analyzers, Git providers, test/coverage adapters, graph renderers, and CI output formatters should have narrow interfaces and independent tests.
