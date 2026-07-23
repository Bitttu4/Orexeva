"""
Shared types for the Orexeva intelligence module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from orexeva.providers.base import ProviderMetadata, ProviderStatus


class CapabilityLevel(str, Enum):
    """Normalized capability levels used by the intelligence pipeline."""

    UNKNOWN = "unknown"
    LOW = "low"
    MODERATE = "moderate"
    GOOD = "good"
    STRONG = "strong"
    EXCELLENT = "excellent"


class RuntimeDecision(str, Enum):
    """Decision outcomes for provider/runtime selection."""

    PREFERRED = "preferred"
    ALTERNATIVE = "alternative"
    UNSUPPORTED = "unsupported"


@dataclass(slots=True, frozen=True)
class SystemResource:
    """Normalized system resource information."""

    cpu: str = ""
    cpu_cores: int | None = None
    cpu_threads: int | None = None
    gpu: str = ""
    ram_total_gb: float | None = None
    storage_total_gb: float | None = None
    storage_free_gb: float | None = None
    os: str = ""
    os_version: str = ""
    architecture: str = ""
    python_version: str = ""


@dataclass(slots=True, frozen=True)
class RuntimeInfo:
    """Normalized runtime state from the provider layer."""

    name: str
    display_name: str
    status: ProviderStatus
    version: str = ""
    installed: bool = False
    supported_platforms: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()


@dataclass(slots=True)
class AnalysisResult:
    """Output of the analysis stage."""

    system: SystemResource
    runtimes: tuple[RuntimeInfo, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)
    registry: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the analysis result."""
        return {
            "system": asdict(self.system),
            "runtimes": [asdict(runtime) for runtime in self.runtimes],
            "config": dict(self.config),
            "registry": dict(self.registry),
        }


@dataclass(slots=True, frozen=True)
class CapabilityScore:
    """A scored capability dimension."""

    name: str
    level: CapabilityLevel
    score: int
    details: str = ""


@dataclass(slots=True, frozen=True)
class RuntimeAssessment:
    """Evaluation data for a runtime provider."""

    name: str
    display_name: str
    supported: bool
    score: int
    status: str
    reasons: tuple[str, ...] = ()


@dataclass(slots=True)
class EvaluationResult:
    """Output of the evaluation stage."""

    capability_scores: tuple[CapabilityScore, ...]
    runtime_assessments: tuple[RuntimeAssessment, ...]
    overall_score: int
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the evaluation result."""
        return {
            "capability_scores": [asdict(score) for score in self.capability_scores],
            "runtime_assessments": [
                asdict(assessment) for assessment in self.runtime_assessments
            ],
            "overall_score": self.overall_score,
            "notes": list(self.notes),
        }


@dataclass(slots=True, frozen=True)
class RuntimeRecommendation:
    """Decision for a runtime provider."""

    name: str
    display_name: str
    decision: RuntimeDecision
    score: int
    reasons: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class ModelRecommendation:
    """Decision for an individual model suggestion."""

    name: str
    role: str
    runtime: str
    decision: RuntimeDecision
    score: int = 0
    reasons: tuple[str, ...] = ()


@dataclass(slots=True)
class DecisionResult:
    """Output of the decision stage."""

    runtime_recommendations: tuple[RuntimeRecommendation, ...]
    model_recommendations: tuple[ModelRecommendation, ...]
    unsupported_runtimes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the decision result."""
        return {
            "runtime_recommendations": [
                asdict(recommendation)
                for recommendation in self.runtime_recommendations
            ],
            "model_recommendations": [
                asdict(recommendation)
                for recommendation in self.model_recommendations
            ],
            "unsupported_runtimes": list(self.unsupported_runtimes),
        }


@dataclass(slots=True, frozen=True)
class AdviceItem:
    """Practical advice item for the user."""

    category: str
    message: str
    priority: int = 0


@dataclass(slots=True)
class AdviceResult:
    """Output of the advice stage."""

    items: tuple[AdviceItem, ...]

    def to_dict(self) -> list[dict[str, Any]]:
        """Serialize advice items."""
        return [asdict(item) for item in self.items]


@dataclass(slots=True, frozen=True)
class WarningItem:
    """Warning item for the final report."""

    message: str
    severity: str = "warning"


@dataclass(slots=True)
class SummaryResult:
    """Final structured intelligence result."""

    system_overview: dict[str, Any]
    capability_summary: list[dict[str, Any]]
    runtime_recommendation: dict[str, Any] | None
    model_recommendations: list[dict[str, Any]]
    advice: list[dict[str, Any]]
    warnings: list[dict[str, Any]]
    upgrade_suggestions: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the final summary."""
        return asdict(self)
