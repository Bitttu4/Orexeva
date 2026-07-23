"""Repair workflow service."""

from __future__ import annotations

from ..context import ExecutionContext
from ..result import RepairResult, ReportSection


class RepairService:
    """Detect likely repair actions without performing destructive changes."""

    def run(self, context: ExecutionContext) -> RepairResult:
        """Run the repair workflow."""
        issues: list[str] = []
        actions: list[str] = []

        installed = context.provider_manager.list_installed()
        if not installed:
            issues.append("No installed providers were detected.")
            actions.append("Install at least one supported runtime provider.")

        default_provider = context.config.get("default_provider", "ollama")
        if default_provider not in context.provider_manager.list_supported():
            issues.append(f"Default provider '{default_provider}' is not registered.")
            actions.append("Update the default provider to a supported runtime.")
        elif default_provider not in installed:
            issues.append(f"Default provider '{default_provider}' is not installed.")
            actions.append("Install or enable the configured default runtime.")

        sections = (
            ReportSection(
                title="Detected Issues",
                lines=tuple(issues) or ("No immediate repair issues were detected.",),
            ),
            ReportSection(
                title="Recommended Actions",
                lines=tuple(actions) or ("No repair action is currently required.",),
            ),
        )

        return RepairResult(
            title="Orexeva Repair Overview",
            summary="Potential repair conditions were checked without performing changes.",
            status="needs_attention" if issues else "healthy",
            sections=sections,
            warnings=tuple(issues),
            metadata={"installed_providers": installed},
        )

