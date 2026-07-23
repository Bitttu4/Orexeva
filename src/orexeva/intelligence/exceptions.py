"""
Orexeva intelligence exceptions.
"""

from __future__ import annotations


class IntelligenceError(Exception):
    """Base exception for intelligence module failures."""


class AnalysisError(IntelligenceError):
    """Raised when system analysis fails."""


class EvaluationError(IntelligenceError):
    """Raised when capability evaluation fails."""


class DecisionError(IntelligenceError):
    """Raised when the decision engine cannot determine a recommendation."""


class AdviceError(IntelligenceError):
    """Raised when user advice cannot be generated."""


class SummaryError(IntelligenceError):
    """Raised when the final summary cannot be produced."""
