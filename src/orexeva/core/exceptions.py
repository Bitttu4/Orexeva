"""Core layer exceptions."""

from __future__ import annotations


class CoreError(Exception):
    """Base exception for the Core layer."""


class CoreExecutionError(CoreError):
    """Raised when a core workflow cannot complete successfully."""


class CoreUnavailableError(CoreError):
    """Raised when a required subsystem is unavailable."""

