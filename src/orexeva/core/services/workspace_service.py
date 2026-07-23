"""Workspace workflow service."""

from __future__ import annotations

from ..context import ExecutionContext
from ..result import ReportSection, WorkspaceResult


class WorkspaceService:
    """Summarize workspace-related configuration and state."""

    def run(self, context: ExecutionContext) -> WorkspaceResult:
        """Run the workspace workflow."""
        sections = (
            ReportSection(
                title="Workspace Configuration",
                lines=(
                    f"default_provider: {context.config.get('default_provider', 'ollama')}",
                    f"default_model: {context.config.get('default_model', 'none')}",
                    f"theme: {context.config.get('theme', 'system')}",
                    f"telemetry: {context.config.get('telemetry', False)}",
                ),
            ),
            ReportSection(
                title="Workspace Readiness",
                lines=(
                    "No workspace scaffolding engine is implemented yet.",
                    "Core can already report the active configuration and provider state.",
                ),
            ),
        )

        return WorkspaceResult(
            title="Orexeva Workspace Overview",
            summary="Workspace-related configuration was collected for future scaffolding support.",
            status="informational",
            sections=sections,
            metadata={"registry_keys": sorted(context.registry.keys())},
        )

