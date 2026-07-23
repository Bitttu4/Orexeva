"""Update workflow service."""

from __future__ import annotations

from orexeva.constants import VERSION

from ..context import ExecutionContext
from ..result import ReportSection, UpdateResult


class UpdateService:
    """Report update-related state and expectations."""

    def run(self, context: ExecutionContext) -> UpdateResult:
        """Run the update workflow."""
        sections = (
            ReportSection(
                title="Update Policy",
                lines=(
                    f"auto_update: {context.config.get('auto_update', True)}",
                    f"check_updates_on_startup: {context.config.get('check_updates_on_startup', True)}",
                    f"orexeva_version: {VERSION}",
                ),
            ),
            ReportSection(
                title="Installed Providers",
                lines=tuple(context.provider_manager.list_installed()) or ("No installed providers detected.",),
            ),
            ReportSection(
                title="Update Notes",
                lines=(
                    "Self-update is not implemented in the Core layer yet.",
                    "The module can still describe the current update posture deterministically.",
                ),
            ),
        )

        return UpdateResult(
            title="Orexeva Update Overview",
            summary="Update-related configuration and provider state were collected.",
            status="informational",
            sections=sections,
            metadata={"version": VERSION},
        )

