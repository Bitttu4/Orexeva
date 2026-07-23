"""Doctor workflow service."""

from __future__ import annotations

from orexeva.intelligence import analyze, advise, decide, evaluate, summarize

from ..context import ExecutionContext
from ..result import DoctorResult, ReportSection


def _lines_from_mapping(mapping: dict[str, object]) -> tuple[str, ...]:
    return tuple(f"{key}: {value}" for key, value in mapping.items())


class DoctorService:
    """Build a structured health report for the current environment."""

    def run(self, context: ExecutionContext) -> DoctorResult:
        """Run the doctor workflow."""
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
                title="System Overview",
                lines=_lines_from_mapping(summary.system_overview),
            ),
            ReportSection(
                title="Capability Summary",
                lines=tuple(
                    f"{item['name']}: {item['score']} ({item['level']})"
                    for item in summary.capability_summary
                ),
            ),
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
                title="Advice",
                lines=tuple(item["message"] for item in summary.advice),
            ),
        )

        metadata = {
            "analysis": analysis.to_dict(),
            "evaluation": evaluation.to_dict(),
            "decision": decision.to_dict(),
            "advice": advice_result.to_dict(),
            "warnings": summary.warnings,
        }

        return DoctorResult(
            title="Orexeva Doctor Report",
            summary=(
                "System analysis completed. Review the report sections for the current "
                "environment state and actionable guidance."
            ),
            status="healthy" if summary.runtime_recommendation else "degraded",
            sections=sections,
            warnings=(),
            metadata=metadata,
        )
