"""
Decision stage for Orexeva intelligence.
"""

from __future__ import annotations

from .types import (
    AnalysisResult,
    DecisionResult,
    EvaluationResult,
    ModelRecommendation,
    RuntimeDecision,
    RuntimeRecommendation,
)


def _runtime_priority(
    name: str,
    display_name: str,
    supported: bool,
    score: int,
) -> RuntimeRecommendation:
    decision = RuntimeDecision.PREFERRED if supported else RuntimeDecision.UNSUPPORTED
    if not supported:
        score = 0
    return RuntimeRecommendation(
        name=name,
        display_name=display_name,
        decision=decision,
        score=score,
        reasons=(
            "Detected and supported." if supported else "Not supported on this system.",
        ),
    )


def _model_recommendations(
    analysis: AnalysisResult,
    preferred_runtime: str,
) -> tuple[ModelRecommendation, ...]:
    ram = analysis.system.ram_total_gb or 0.0
    gpu = analysis.system.gpu.lower()

    recommendations: list[ModelRecommendation] = []
    if ram >= 32 and any(token in gpu for token in ("nvidia", "rtx", "m1", "m2", "m3", "apple")):
        recommendations.append(
            ModelRecommendation(
                name="general-purpose-code-assistant",
                role="Lead Software Engineer",
                runtime=preferred_runtime,
                decision=RuntimeDecision.PREFERRED,
                score=95,
                reasons=("High RAM and GPU capacity support a larger local code model.",),
            )
        )
    elif ram >= 16:
        recommendations.append(
            ModelRecommendation(
                name="balanced-code-assistant",
                role="Quick Assistant",
                runtime=preferred_runtime,
                decision=RuntimeDecision.PREFERRED,
                score=80,
                reasons=("Moderate hardware is suitable for a compact local code model.",),
            )
        )
    elif ram >= 8:
        recommendations.append(
            ModelRecommendation(
                name="lightweight-code-assistant",
                role="Quick Assistant",
                runtime=preferred_runtime,
                decision=RuntimeDecision.ALTERNATIVE,
                score=60,
                reasons=("Entry-level hardware should stay with a lightweight quantized model.",),
            )
        )
    else:
        recommendations.append(
            ModelRecommendation(
                name="cloud-or-remote-assistant",
                role="Fallback",
                runtime=preferred_runtime,
                decision=RuntimeDecision.UNSUPPORTED,
                score=0,
                reasons=("Local hardware is below the safe minimum for recommended local models.",),
            )
        )

    return tuple(recommendations)


def decide(analysis: AnalysisResult, evaluation: EvaluationResult) -> DecisionResult:
    """Turn analysis and evaluation into runtime and model recommendations."""
    runtime_recommendations: list[RuntimeRecommendation] = []
    unsupported_runtimes: list[str] = []

    for assessment in evaluation.runtime_assessments:
        recommendation = _runtime_priority(
            assessment.name,
            assessment.display_name,
            assessment.supported,
            assessment.score,
        )
        runtime_recommendations.append(recommendation)
        if recommendation.decision == RuntimeDecision.UNSUPPORTED:
            unsupported_runtimes.append(assessment.name)

    runtime_recommendations.sort(key=lambda item: (item.decision != RuntimeDecision.PREFERRED, -item.score, item.name))
    preferred_runtime = (
        next(
            (item.name for item in runtime_recommendations if item.decision == RuntimeDecision.PREFERRED),
            "none",
        )
    )
    model_recommendations = _model_recommendations(analysis, preferred_runtime)

    return DecisionResult(
        runtime_recommendations=tuple(runtime_recommendations),
        model_recommendations=model_recommendations,
        unsupported_runtimes=tuple(unsupported_runtimes),
    )
