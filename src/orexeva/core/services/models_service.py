"""Models workflow service."""

from __future__ import annotations

from orexeva.providers import ProviderError

from ..context import ExecutionContext
from ..result import ModelResult, ReportSection


class ModelsService:
    """Summarize installed models across available providers."""

    def run(self, context: ExecutionContext) -> ModelResult:
        """Run the models workflow."""
        provider_names = context.provider_manager.list_installed()
        provider_lines: list[str] = []
        model_lines: list[str] = []
        warnings: list[str] = []

        if not provider_names:
            provider_lines.append("No installed providers were detected.")

        for name in provider_names:
            provider = context.provider_manager.get(name)
            provider_lines.append(f"{provider.metadata.display_name} ({provider.metadata.name})")
            try:
                models = provider.list_models()
            except ProviderError as exc:
                warnings.append(f"{provider.metadata.display_name}: {exc}")
                continue

            if not models:
                model_lines.append(f"{provider.metadata.display_name}: no models installed.")
                continue

            for model in models:
                model_name = model.get("name", "unknown")
                model_lines.append(f"{provider.metadata.display_name}: {model_name}")

        sections = (
            ReportSection(title="Installed Providers", lines=tuple(provider_lines)),
            ReportSection(title="Installed Models", lines=tuple(model_lines) or ("No installed models were found.",)),
        )

        return ModelResult(
            title="Orexeva Models Report",
            summary="Installed providers and models were collected from the provider layer.",
            status="ready" if provider_names else "limited",
            sections=sections,
            warnings=tuple(warnings),
            metadata={"provider_count": len(provider_names)},
        )

