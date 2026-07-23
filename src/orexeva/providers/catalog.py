"""
Provider catalog.

This module is the single source of truth for built-in provider classes.
"""

from __future__ import annotations

from typing import Type

from .base import BaseProvider, ProviderCategory, ProviderMetadata
from .exceptions import ProviderAlreadyRegisteredError, ProviderError, ProviderNotFoundError


_PROVIDER_REGISTRY: dict[str, Type[BaseProvider]] = {}


def _provider_metadata(provider: Type[BaseProvider]) -> ProviderMetadata:
    """Return provider metadata without forcing instantiation when possible."""
    metadata = getattr(provider, "_METADATA", None)
    if isinstance(metadata, ProviderMetadata):
        return metadata
    return provider().metadata


def register_provider(provider: Type[BaseProvider]) -> None:
    """Register a provider class in the catalog."""
    name = _provider_metadata(provider).name.strip().lower()
    if not name:
        raise ProviderError("Provider name cannot be empty.")
    if name in _PROVIDER_REGISTRY:
        raise ProviderAlreadyRegisteredError(
            f"Provider '{name}' is already registered."
        )
    _PROVIDER_REGISTRY[name] = provider


def unregister_provider(name: str) -> None:
    """Remove a provider from the catalog if it exists."""
    _PROVIDER_REGISTRY.pop(name.strip().lower(), None)


def get_provider(name: str) -> Type[BaseProvider]:
    """Return a registered provider class."""
    provider = _PROVIDER_REGISTRY.get(name.strip().lower())
    if provider is None:
        raise ProviderNotFoundError(f"Provider '{name}' is not registered.")
    return provider


def provider_exists(name: str) -> bool:
    """Return True when a provider is registered."""
    return name.strip().lower() in _PROVIDER_REGISTRY


def list_providers() -> list[str]:
    """Return registered provider names."""
    return sorted(_PROVIDER_REGISTRY.keys())


def list_by_category(category: ProviderCategory) -> list[str]:
    """Return registered provider names filtered by category."""
    return sorted(
        name
        for name, provider in _PROVIDER_REGISTRY.items()
        if _provider_metadata(provider).category == category
    )


def get_metadata(name: str) -> ProviderMetadata:
    """Return metadata for a registered provider."""
    return _provider_metadata(get_provider(name))


def list_metadata() -> list[ProviderMetadata]:
    """Return metadata for every registered provider."""
    return [_provider_metadata(provider) for provider in _PROVIDER_REGISTRY.values()]


def clear_catalog() -> None:
    """Remove all registered providers."""
    _PROVIDER_REGISTRY.clear()


def provider_count() -> int:
    """Return the number of registered providers."""
    return len(_PROVIDER_REGISTRY)
