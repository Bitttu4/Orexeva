"""
Final summary stage for Orexeva intelligence.
"""

from __future__ import annotations

from dataclasses import asdict

from .types import (
    AdviceResult,
    AnalysisResult,
    DecisionResult,
    EvaluationResult,
    RuntimeDecision,
    SummaryResult,
)


def summarize(
    analysis: AnalysisResult,
    evaluation: EvaluationResult,
    decision: DecisionResult,
    advice: AdviceResult,
) -> SummaryResult:
    """Combine all intelligence stages into a structured summary."""
    system_overview = {
        "os": analysis.system.os,
        "os_version": analysis.system.os_version,
        "architecture": analysis.system.architecture,
        "cpu": analysis.system.cpu,
        "cpu_cores": analysis.system.cpu_cores,
        "cpu_threads": analysis.system.cpu_threads,
        "gpu": analysis.system.gpu,
        "ram_total_gb": analysis.system.ram_total_gb,
        "storage_total_gb": analysis.system.storage_total_gb,
        "storage_free_gb": analysis.system.storage_free_gb,
        "python_version": analysis.system.python_version,
    }

    capability_summary = [asdict(score) for score in evaluation.capability_scores]
    runtime_recommendation = None
    for recommendation in decision.runtime_recommendations:
        if recommendation.decision == RuntimeDecision.PREFERRED:
            runtime_recommendation = asdict(recommendation)
            break
    model_recommendations = [
        asdict(recommendation) for recommendation in decision.model_recommendations
    ]
    warnings = [
        {"message": item.message, "severity": "warning"}
        for item in advice.items
        if item.priority > 0
    ]
    upgrade_suggestions = [
        item.message
        for item in advice.items
        if item.category in {"ram", "storage", "gpu"}
    ]

    return SummaryResult(
        system_overview=system_overview,
        capability_summary=capability_summary,
        runtime_recommendation=runtime_recommendation,
        model_recommendations=model_recommendations,
        advice=advice.to_dict(),
        warnings=warnings,
        upgrade_suggestions=upgrade_suggestions,
    )
