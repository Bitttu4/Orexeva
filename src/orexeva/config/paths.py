"""
Orexeva configuration paths.

Provides cross-platform application directories.
"""

from __future__ import annotations

import os
import platform
from pathlib import Path

APP_NAME = "Orexeva"


def _base_directory() -> Path:
    """
    Return the platform-specific application directory.
    """

    system = platform.system()

    if system == "Windows":
        base = os.getenv("LOCALAPPDATA")
        if base:
            return Path(base) / APP_NAME

    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME

    elif system == "Linux":
        return Path.home() / ".local" / "share" / APP_NAME

    # Fallback
    return Path.home() / f".{APP_NAME.lower()}"


BASE_DIR = _base_directory()

CONFIG_FILE = BASE_DIR / "config.json"

MODELS_DIR = BASE_DIR / "models"
CACHE_DIR = BASE_DIR / "cache"
LOGS_DIR = BASE_DIR / "logs"
DOWNLOADS_DIR = BASE_DIR / "downloads"
RUNTIME_DIR = BASE_DIR / "runtime"
TEMP_DIR = BASE_DIR / "temp"


def create_directories() -> None:
    """
    Create all required Orexeva directories.
    """

    for directory in (
        BASE_DIR,
        MODELS_DIR,
        CACHE_DIR,
        LOGS_DIR,
        DOWNLOADS_DIR,
        RUNTIME_DIR,
        TEMP_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def get_paths() -> dict[str, Path]:
    """
    Return all Orexeva paths.
    """

    return {
        "base": BASE_DIR,
        "config": CONFIG_FILE,
        "models": MODELS_DIR,
        "cache": CACHE_DIR,
        "logs": LOGS_DIR,
        "downloads": DOWNLOADS_DIR,
        "runtime": RUNTIME_DIR,
        "temp": TEMP_DIR,
    }