"""Clean workflow service."""

from __future__ import annotations

from orexeva.config.paths import get_paths

from ..context import ExecutionContext
from ..result import CleanResult, ReportSection


class CleanService:
    """Report cleanup targets without deleting anything."""

    def run(self, context: ExecutionContext) -> CleanResult:
        """Run the clean workflow."""
        paths = get_paths()
        cache_enabled = context.config.get("cache_enabled", True)

        sections = (
            ReportSection(
                title="Cleanup Targets",
                lines=(
                    f"cache: {paths['cache']}",
                    f"logs: {paths['logs']}",
                    f"downloads: {paths['downloads']}",
                    f"temp: {paths['temp']}",
                ),
            ),
            ReportSection(
                title="Cleanup Notes",
                lines=(
                    "The Core layer only reports cleanup candidates at this stage.",
                    f"Cache management is {'enabled' if cache_enabled else 'disabled'} in config.",
                ),
            ),
        )

        return CleanResult(
            title="Orexeva Clean Overview",
            summary="Cleanup candidates were identified from the local configuration.",
            status="informational",
            sections=sections,
            metadata={"paths": {key: str(value) for key, value in paths.items()}},
        )

