"""
Practical advice stage for Orexeva intelligence.
"""

from __future__ import annotations

from .types import AdviceItem, AdviceResult, AnalysisResult, DecisionResult, EvaluationResult


def advise(
    analysis: AnalysisResult,
    evaluation: EvaluationResult,
    decision: DecisionResult,
) -> AdviceResult:
    """Generate practical system advice from the detected state."""
    items: list[AdviceItem] = []

    ram = analysis.system.ram_total_gb or 0.0
    storage_free = analysis.system.storage_free_gb or 0.0
    gpu = analysis.system.gpu.lower()

    if ram < 16:
        items.append(
            AdviceItem(
                category="ram",
                message="Consider upgrading to at least 16 GB RAM for smoother local model usage.",
                priority=2,
            )
        )

    if storage_free < 100:
        items.append(
            AdviceItem(
                category="storage",
                message="Free up disk space before pulling multiple model checkpoints.",
                priority=2,
            )
        )

    if "nvidia" not in gpu and "rtx" not in gpu and ram >= 16:
        items.append(
            AdviceItem(
                category="gpu",
                message="If you want faster local inference, a CUDA-capable NVIDIA GPU can help.",
                priority=1,
            )
        )

    if decision.unsupported_runtimes:
        items.append(
            AdviceItem(
                category="runtime",
                message="Some runtimes are unsupported on this system; stick to the recommended runtime path.",
                priority=1,
            )
        )

    if not items:
        items.append(
            AdviceItem(
                category="general",
                message="The system looks healthy for local AI development.",
                priority=0,
            )
        )

    return AdviceResult(items=tuple(items))
