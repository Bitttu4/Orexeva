"""Orexeva intelligence module."""

from __future__ import annotations

from .advise import advise
from .analyze import analyze
from .decide import decide
from .engine import run, run_intelligence
from .evaluate import evaluate
from .exceptions import (
    AdviceError,
    AnalysisError,
    DecisionError,
    EvaluationError,
    IntelligenceError,
    SummaryError,
)
from .summarize import summarize
from .types import (
    AdviceItem,
    AdviceResult,
    AnalysisResult,
    CapabilityLevel,
    CapabilityScore,
    DecisionResult,
    EvaluationResult,
    ModelRecommendation,
    RuntimeDecision,
    RuntimeInfo,
    RuntimeRecommendation,
    SummaryResult,
    SystemResource,
    WarningItem,
)

__all__ = [
    "advise",
    "analyze",
    "decide",
    "run",
    "run_intelligence",
    "evaluate",
    "summarize",
    "IntelligenceError",
    "AnalysisError",
    "EvaluationError",
    "DecisionError",
    "AdviceError",
    "SummaryError",
    "AdviceItem",
    "AdviceResult",
    "AnalysisResult",
    "CapabilityLevel",
    "CapabilityScore",
    "DecisionResult",
    "EvaluationResult",
    "ModelRecommendation",
    "RuntimeDecision",
    "RuntimeInfo",
    "RuntimeRecommendation",
    "SummaryResult",
    "SystemResource",
    "WarningItem",
]
