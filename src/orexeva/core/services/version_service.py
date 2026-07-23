"""Version workflow service."""

from __future__ import annotations

from orexeva.constants import APP_NAME, VERSION

from ..context import ExecutionContext
from ..result import ReportSection, VersionResult


class VersionService:
    """Report the current Orexeva version."""

    def run(self, context: ExecutionContext) -> VersionResult:
        """Run the version workflow."""
        sections = (
            ReportSection(
                title="Build Information",
                lines=(
                    f"application: {APP_NAME}",
                    f"version: {VERSION}",
                    f"telemetry: {context.config.get('telemetry', False)}",
                ),
            ),
        )

        return VersionResult(
            title="Orexeva Version",
            summary="Current application version and basic build information.",
            status="ok",
            sections=sections,
            metadata={"application": APP_NAME, "version": VERSION},
        )

