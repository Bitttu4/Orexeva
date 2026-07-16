"""
Orexeva Platform Module.

Provides cross-platform hardware and operating system
detection for Windows, Linux and macOS.
"""

from .detector import detect

__all__ = [
    "detect",
]