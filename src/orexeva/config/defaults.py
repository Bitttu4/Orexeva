"""
Orexeva default configuration.
"""

from __future__ import annotations

DEFAULT_CONFIG: dict = {
    # Application
    "theme": "system",
    "language": "en",

    # Updates
    "auto_update": True,
    "check_updates_on_startup": True,

    # Privacy
    "telemetry": False,

    # AI
    "default_provider": "ollama",
    "default_model": None,

    # Downloads
    "max_parallel_downloads": 3,

    # Cache
    "cache_enabled": True,
    "cache_size_gb": 20,

    # Runtime
    "auto_start_runtime": False,

    # Logging
    "log_level": "INFO",
}