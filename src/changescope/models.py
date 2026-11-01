"""Typed data structures used by ChangeScope."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Dependency:
    source: str
    target: str
    kind: str
    line: int | None = None


@dataclass
class AnalysisResult:
    root: str
    changed_files: list[str]
    affected_files: list[str] = field(default_factory=list)
    recommended_tests: list[str] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    risk: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)
