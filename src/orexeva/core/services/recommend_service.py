"""Recommendation workflow service."""

from __future__ import annotations

from orexeva.intelligence import analyze, advise, decide, evaluate, summarize

from ..context import ExecutionContext
from ..result import RecommendationResult, ReportSection


class RecommendService:
    """Build a deterministic recommendation report."""

    def run(self, context: ExecutionContext) -> RecommendationResult:
        """Run the recommendation workflow."""
        analysis = analyze(
            provider_manager=context.provider_manager,
            config=context.config,
            registry=context.registry,
        )
        evaluation = evaluate(analysis)
        decision = decide(analysis, evaluation)
        advice_result = advise(analysis, evaluation, decision)
        summary = summarize(analysis, evaluation, decision, advice_result)

        sections = (
            ReportSection(
                title="Runtime Recommendation",
                lines=(
                    (
                        f"{summary.runtime_recommendation['display_name']} "
                        f"({summary.runtime_recommendation['decision']})"
                        if summary.runtime_recommendation
                        else "No preferred runtime could be determined on this system."
                    ),
                ),
            ),
            ReportSection(
                title="Model Recommendations",
                lines=tuple(
                    f"{item['role']}: {item['name']} via {item['runtime']} "
                    f"({item['decision']}, score={item['score']})"
                    for item in summary.model_recommendations
                ),
            ),
            ReportSection(
                title="Capability Summary",
                lines=tuple(
                    f"{item['name']}: {item['score']} ({item['level']})"
                    for item in summary.capability_summary
                ),
            ),
            ReportSection(
                title="Recommendation Notes",
                lines=tuple(item["message"] for item in summary.warnings)
                or (
                    "No preferred runtime could be determined on this system.",
                ),
            ),
        )

        return RecommendationResult(
            title="Orexeva Recommendation Report",
            summary=(
                "Deterministic runtime and model recommendations generated from the "
                "current machine state."
            ),
            status="ready" if summary.runtime_recommendation else "limited",
            sections=sections,
            warnings=(),
            metadata={
                "summary": summary.to_dict(),
                "warnings": tuple(item["message"] for item in summary.warnings),
            },
        )
