"""
Orexeva registry schema.
"""

from __future__ import annotations

DEFAULT_REGISTRY: dict = {
    # Registry metadata
    "registry_version": 1,

    # Installed AI models
    "models": {},

    # Installed providers
    "providers": {},

    # Download manager state
    "downloads": {
        "current": None,
        "history": [],
    },

    # Runtime information
    "runtime": {
        "provider": None,
        "model": None,
        "status": "idle",
    },

    # Internal metadata
    "metadata": {
        "created_at": None,
        "updated_at": None,
        "orexeva_version": "0.1.0-alpha.1",
    },
}