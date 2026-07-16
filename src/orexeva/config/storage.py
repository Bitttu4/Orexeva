"""
Configuration loader.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from .defaults import DEFAULT_CONFIG
from .paths import CONFIG_FILE, create_directories


def load_config() -> dict[str, Any]:
    """
    Load configuration from disk.

    If the config file does not exist,
    it is created automatically.
    """

    create_directories()

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return deepcopy(DEFAULT_CONFIG)

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            user_config = json.load(file)

    except Exception:
        save_config(DEFAULT_CONFIG)
        return deepcopy(DEFAULT_CONFIG)

    config = deepcopy(DEFAULT_CONFIG)
    config.update(user_config)

    return config


def save_config(config: dict[str, Any]) -> None:
    """
    Save configuration to disk.
    """

    create_directories()

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def reset_config() -> dict[str, Any]:
    """
    Reset configuration to defaults.
    """

    save_config(DEFAULT_CONFIG)

    return deepcopy(DEFAULT_CONFIG)