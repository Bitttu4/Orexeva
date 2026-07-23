"""Setup workflow service."""

from __future__ import annotations

from orexeva.intelligence import analyze, advise, decide, evaluate, summarize

from ..context import ExecutionContext
from ..result import ReportSection, SetupResult


class SetupService:
    """Build a setup readiness report."""

    def run(self, context: ExecutionContext) -> SetupResult:
        """Run the setup workflow."""
        analysis = analyze(
            provider_manager=context.provider_manager,
            config=context.config,
            registry=context.registry,
        )
        evaluation = evaluate(analysis)
        decision = decide(analysis, evaluation)
        advice_result = advise(analysis, evaluation, decision)
        summary = summarize(analysis, evaluation, decision, advice_result)

        next_steps = (
            "Review the recommended runtime.",
            "Install or enable the recommended runtime outside Orexeva if needed.",
            "Pull the suggested model after the runtime is available.",
            "Re-run `orexeva doctor` to confirm the environment is ready.",
        )

        sections = (
            ReportSection(
                title="Recommended Runtime",
                lines=(
                    (
                        f"{summary.runtime_recommendation['display_name']} "
                        f"({summary.runtime_recommendation['decision']})"
                        if summary.runtime_recommendation
                        else "No preferred runtime is available on this system."
                    ),
                ),
            ),
            ReportSection(
                title="Recommended Models",
                lines=tuple(
                    f"{item['role']}: {item['name']} via {item['runtime']}"
                    for item in summary.model_recommendations
                ),
            ),
            ReportSection(
                title="Setup Steps",
                lines=next_steps,
            ),
        )

        return SetupResult(
            title="Orexeva Setup Plan",
            summary=(
                "Orexeva analyzed the system and prepared a setup plan based on the "
                "current deterministic recommendations."
            ),
            status="ready" if summary.runtime_recommendation else "planning",
            sections=sections,
            warnings=tuple(item["message"] for item in summary.warnings),
            metadata={
                "auto_start_runtime": context.config.get("auto_start_runtime", False),
                "summary": summary.to_dict(),
            },
        )

