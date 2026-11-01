"""Markdown and JSON report rendering."""

from __future__ import annotations

import json

from changescope.models import AnalysisResult


def render_json(result: AnalysisResult) -> str:
    """Render a stable, human-readable JSON report."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True)


def render_markdown(result: AnalysisResult) -> str:
    """Render an impact report with explicit caveats."""
    lines = [
        "# ChangeScope Impact Report",
        "",
        f"**Risk indicator:** {result.risk.upper()}",
        "",
        "> This is static, best-effort impact analysis—not a guarantee that a change will or will not break behavior.",
        "",
        "## Changed files",
        "",
    ]
    if result.changed_files:
        lines.extend(f"- `{path}`" for path in result.changed_files)
    else:
        lines.append("- No changed files detected.")
    lines.extend(["", "## Potentially affected files", ""])
    if result.affected_files:
        lines.extend(f"- `{path}`" for path in result.affected_files)
    else:
        lines.append("- No downstream dependencies identified.")
    lines.extend(["", "## Candidate tests", ""])
    if result.recommended_tests:
        lines.extend(f"- `{path}`" for path in result.recommended_tests)
    else:
        lines.append("- No candidate tests identified from static import relationships.")
    lines.extend(["", "## Warnings", ""])
    if result.warnings:
        lines.extend(f"- {warning}" for warning in result.warnings)
    else:
        lines.append("- No parser or file-reading warnings.")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Dynamic imports, reflection, runtime dispatch, and generated code may be missed.",
            "- Test recommendations are candidates; run your full test suite before merging.",
            "- The risk indicator is a coarse heuristic, not a defect probability.",
            "",
        ]
    )
    return "\n".join(lines)
