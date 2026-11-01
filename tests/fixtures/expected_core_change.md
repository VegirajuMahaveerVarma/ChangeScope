# ChangeScope Impact Report

**Risk indicator:** LOW

**Analysis scope:** potential impact only; recommendations are advisory.

> Static analysis cannot guarantee that a change will or will not break behavior.

## Changed files

- `src/demo_pkg/core.py`

## Potentially affected files

- `src/demo_pkg/service.py`
- `tests/test_service.py`

## Dependency evidence

- `demo_pkg.service` imports `demo_pkg.core` (line 1)
- `tests.test_service` imports `demo_pkg.service` (line 1)

## Candidate tests

- `tests/test_service.py`

## Warnings

- No parser or file-reading warnings.

## Limitations

- Dynamic imports, reflection, runtime dispatch, and generated code may be missed.
- Test recommendations are candidates; run your full test suite before merging.
- The risk indicator is a coarse heuristic, not a defect probability.
