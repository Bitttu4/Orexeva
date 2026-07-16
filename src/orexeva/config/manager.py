"""
Configuration manager.
"""

from __future__ import annotations

from typing import Any

from .storage import (
    load_config,
    save_config,
    reset_config,
)


class Config:
    """
    Orexeva configuration manager.
    """

    def __init__(self) -> None:
        self._config = load_config()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        """
        self._config[key] = value

    def save(self) -> None:
        """
        Save configuration.
        """
        save_config(self._config)

    def reset(self) -> None:
        """
        Reset configuration.
        """
        self._config = reset_config()

    def all(self) -> dict[str, Any]:
        """
        Return all configuration values.
        """
        return self._config.copy()