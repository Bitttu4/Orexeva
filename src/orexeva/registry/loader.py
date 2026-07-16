"""
Orexeva registry loader.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .storage import (
    registry_exists,
    read_registry,
    write_registry,
)
from .schema import DEFAULT_REGISTRY


def load_registry() -> dict[str, Any]:
    """
    Load the registry from disk.
    If it doesn't exist, create it with defaults.
    """

    if not registry_exists():
        save_registry(DEFAULT_REGISTRY)
        return deepcopy(DEFAULT_REGISTRY)

    registry = deepcopy(DEFAULT_REGISTRY)
    registry.update(read_registry())

    return registry


def save_registry(registry: dict[str, Any]) -> None:
    """
    Save the registry to disk.
    """

    write_registry(registry)


def reset_registry() -> dict[str, Any]:
    """
    Reset registry to default values.
    """

    save_registry(DEFAULT_REGISTRY)

    return deepcopy(DEFAULT_REGISTRY)