"""
Intelligence engine orchestration.
"""

from __future__ import annotations

from orexeva.config import Config
from orexeva.providers import ProviderManager
from orexeva.registry.loader import load_registry

from .advise import advise
from .analyze import analyze
from .decide import decide
from .evaluate import evaluate
from .summarize import summarize
from .types import SummaryResult


def run_intelligence(
    provider_manager: ProviderManager | None = None,
    config: Config | None = None,
) -> SummaryResult:
    """Run the full intelligence workflow."""
    try:
        registry = load_registry()
    except Exception:
        registry = {}
    analysis = analyze(
        provider_manager=provider_manager,
        config=config,
        registry=registry,
    )
    evaluation = evaluate(analysis)
    decision = decide(analysis, evaluation)
    advice_result = advise(analysis, evaluation, decision)
    return summarize(analysis, evaluation, decision, advice_result)


def run(
    provider_manager: ProviderManager | None = None,
    config: Config | None = None,
) -> SummaryResult:
    """Compatibility wrapper for the intelligence engine."""
    return run_intelligence(provider_manager=provider_manager, config=config)
