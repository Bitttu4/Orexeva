"""
Provider manager.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .base import BaseProvider, ProviderMetadata
from .catalog import (
    get_provider,
    get_metadata,
    list_providers,
    provider_exists,
    register_provider,
)
from .exceptions import ProviderError


@dataclass(slots=True)
class ProviderManager:
    """Lightweight provider registry and discovery manager."""

    _providers: dict[str, BaseProvider] = field(default_factory=dict)

    def register(self, provider: BaseProvider) -> None:
        """Register a provider instance."""
        name = provider.metadata.name.strip().lower()
        if not name:
            raise ProviderError("Provider name cannot be empty.")
        self._providers[name] = provider

    def register_class(self, provider: type[BaseProvider]) -> None:
        """Register a provider class in the shared catalog."""
        register_provider(provider)

    def discover(self) -> list[BaseProvider]:
        """Instantiate and register all known providers that are importable."""
        from . import runtimes

        discovered: list[BaseProvider] = []
        for provider_cls in runtimes.PROVIDER_TYPES:
            provider = provider_cls()
            self.register(provider)
            discovered.append(provider)
        return discovered

    def get(self, name: str) -> BaseProvider:
        """Return a registered provider instance or instantiate it from the catalog."""
        key = name.strip().lower()
        provider = self._providers.get(key)
        if provider is not None:
            return provider
        provider_cls = get_provider(key)
        provider = provider_cls()
        self._providers[key] = provider
        return provider

    def list_supported(self) -> list[str]:
        """Return all provider names declared in the catalog."""
        return list_providers()

    def list_installed(self) -> list[str]:
        """Return provider names that are installed."""
        installed: list[str] = []
        for name in self.list_supported():
            provider = self._providers.get(name)
            if provider is None:
                provider = get_provider(name)()
                self._providers[name] = provider
            if provider.is_installed():
                installed.append(name)
        return sorted(installed)

    def validate(self, name: str) -> bool:
        """Validate provider state by checking installation and verification."""
        provider = self.get(name)
        return provider.is_installed() and provider.verify()

    def metadata(self, name: str) -> ProviderMetadata:
        """Return metadata for a provider."""
        if provider_exists(name):
            return get_metadata(name)
        return self.get(name).metadata

    def clear(self) -> None:
        """Clear registered provider instances."""
        self._providers.clear()

    def items(self) -> list[tuple[str, BaseProvider]]:
        """Return registered providers as name/provider pairs."""
        return sorted(self._providers.items())

    def extend(self, providers: Iterable[BaseProvider]) -> None:
        """Register multiple provider instances."""
        for provider in providers:
            self.register(provider)

    def installed_metadata(self) -> list[ProviderMetadata]:
        """Return metadata for installed providers."""
        return [self.get(name).metadata for name in self.list_installed()]
