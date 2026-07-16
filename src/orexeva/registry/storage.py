"""
Orexeva registry database.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config.paths import BASE_DIR

REGISTRY_FILE = BASE_DIR / "registry.json"


def registry_exists() -> bool:
    """
    Check whether the registry file exists.
    """
    return REGISTRY_FILE.exists()


def read_registry() -> dict[str, Any]:
    """
    Read registry from disk.
    """

    with REGISTRY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_registry(registry: dict[str, Any]) -> None:
    """
    Write registry to disk.
    """

    BASE_DIR.mkdir(parents=True, exist_ok=True)

    with REGISTRY_FILE.open("w", encoding="utf-8") as file:
        json.dump(registry, file, indent=4)


def registry_path() -> Path:
    """
    Return registry file path.
    """

    return REGISTRY_FILE