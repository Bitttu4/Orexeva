"""Shared result models for Orexeva core services."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class ReportSection:
    """A named section in a command result."""

    title: str
    lines: tuple[str, ...] = ()


@dataclass(slots=True)
class ReportResult:
    """Base structured result returned by core services."""

    title: str
    summary: str
    status: str = "ok"
    sections: tuple[ReportSection, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result."""
        return asdict(self)

    def to_text(self) -> str:
        """Render the result as plain text for CLI output."""
        lines = [self.title, "", self.summary]
        for section in self.sections:
            lines.append("")
            lines.append(section.title)
            for line in section.lines:
                lines.append(f"- {line}")
        if self.warnings:
            lines.append("")
            lines.append("Warnings")
            for warning in self.warnings:
                lines.append(f"- {warning}")
        return "\n".join(lines).strip()


@dataclass(slots=True)
class DoctorResult(ReportResult):
    """Result returned by the doctor workflow."""


@dataclass(slots=True)
class SetupResult(ReportResult):
    """Result returned by the setup workflow."""


@dataclass(slots=True)
class RecommendationResult(ReportResult):
    """Result returned by the recommendation workflow."""


@dataclass(slots=True)
class ModelResult(ReportResult):
    """Result returned by the models workflow."""


@dataclass(slots=True)
class WorkspaceResult(ReportResult):
    """Result returned by the workspace workflow."""


@dataclass(slots=True)
class UpdateResult(ReportResult):
    """Result returned by the update workflow."""


@dataclass(slots=True)
class RepairResult(ReportResult):
    """Result returned by the repair workflow."""


@dataclass(slots=True)
class CleanResult(ReportResult):
    """Result returned by the clean workflow."""


@dataclass(slots=True)
class VersionResult(ReportResult):
    """Result returned by the version workflow."""
