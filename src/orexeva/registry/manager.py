"""
Orexeva registry manager.
"""

from __future__ import annotations

from typing import Any

from .loader import (
    load_registry,
    save_registry,
    reset_registry,
)


class Registry:
    """
    Orexeva registry manager.
    """

    def __init__(self) -> None:
        self._registry = load_registry()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a registry value.
        """
        return self._registry.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a registry value.
        """
        self._registry[key] = value

    def save(self) -> None:
        """
        Save registry.
        """
        save_registry(self._registry)

    def reset(self) -> None:
        """
        Reset registry.
        """
        self._registry = reset_registry()

    def all(self) -> dict[str, Any]:
        """
        Return the complete registry.
        """
        return self._registry.copy()