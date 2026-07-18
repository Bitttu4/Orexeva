"""
Provider Catalog

Central registry for all Orexeva providers.
"""

from __future__ import annotations

from typing import Type

from .base import BaseProvider, ProviderCategory
from .exceptions import (
    ProviderAlreadyRegisteredError,
    ProviderError,
    ProviderNotFoundError,
)

# ==========================================================
# Internal Registry
# ==========================================================

_PROVIDER_REGISTRY: dict[str, Type[BaseProvider]] = {}


# ==========================================================
# Registration
# ==========================================================


def register_provider(provider: Type[BaseProvider]) -> None:
    """
    Register a provider class.
    """

    name = provider.metadata.name.strip().lower()

    if not name:
        raise ProviderError("Provider name cannot be empty.")

    if name in _PROVIDER_REGISTRY:
        raise ProviderAlreadyRegisteredError(
            f"Provider '{name}' is already registered."
        )

    _PROVIDER_REGISTRY[name] = provider


def unregister_provider(name: str) -> None:
    """
    Remove a provider from the catalog.
    """

    _PROVIDER_REGISTRY.pop(name.strip().lower(), None)


# ==========================================================
# Lookup
# ==========================================================


def get_provider(name: str) -> Type[BaseProvider]:
    """
    Return a registered provider class.
    """

    provider = _PROVIDER_REGISTRY.get(name.strip().lower())

    if provider is None:
        raise ProviderNotFoundError(
            f"Provider '{name}' is not registered."
        )

    return provider


def provider_exists(name: str) -> bool:
    """
    Return True if a provider exists.
    """

    return name.strip().lower() in _PROVIDER_REGISTRY


# ==========================================================
# Listing
# ==========================================================


def list_providers() -> list[str]:
    """
    Return all registered provider names.
    """

    return sorted(_PROVIDER_REGISTRY.keys())


def list_by_category(
    category: ProviderCategory,
) -> list[str]:
    """
    Return provider names belonging to a category.
    """

    return sorted(
        [
            name
            for name, provider in _PROVIDER_REGISTRY.items()
            if provider.metadata.category == category
        ]
    )


# ==========================================================
# Utilities
# ==========================================================


def clear_catalog() -> None:
    """
    Remove every registered provider.
    """

    _PROVIDER_REGISTRY.clear()


def provider_count() -> int:
    """
    Return the total number of registered providers.
    """

    return len(_PROVIDER_REGISTRY)