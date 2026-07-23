"""Execution context shared across core services."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from orexeva.config import Config
from orexeva.config.defaults import DEFAULT_CONFIG
from orexeva.providers import ProviderManager
from orexeva.registry.loader import load_registry

@dataclass(slots=True)
class _FallbackConfig:
    """In-memory configuration used when the frozen config loader cannot initialize."""

    _config: dict[str, Any] = field(default_factory=lambda: dict(DEFAULT_CONFIG))

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def all(self) -> dict[str, Any]:
        return self._config.copy()


@dataclass(slots=True)
class ExecutionContext:
    """Container for shared configuration, registry, and provider state."""

    config: Config
    registry: dict[str, Any]
    provider_manager: ProviderManager
    cache: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, discover_providers: bool = True) -> "ExecutionContext":
        """Build a context from the frozen subsystems."""
        try:
            config: Config | _FallbackConfig = Config()
        except Exception:
            config = _FallbackConfig()

        try:
            registry = load_registry()
        except Exception:
            registry = {}

        provider_manager = ProviderManager()
        if discover_providers:
            try:
                provider_manager.discover()
            except Exception:
                pass

        return cls(
            config=config,
            registry=registry,
            provider_manager=provider_manager,
        )
