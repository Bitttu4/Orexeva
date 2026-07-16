"""
Cross-platform system detector.
"""

from __future__ import annotations

import platform
from typing import Any

from .linux import get_linux_info
from .macos import get_macos_info
from .windows import get_windows_info


def detect() -> dict[str, Any]:
    """
    Detect the current operating system and return
    standardized platform information.
    """

    system = platform.system()

    if system == "Windows":
        return get_windows_info()

    if system == "Linux":
        return get_linux_info()

    if system == "Darwin":
        return get_macos_info()

    raise NotImplementedError(
        f"Unsupported operating system: {system}"
    )