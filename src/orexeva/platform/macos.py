"""
macOS platform detection.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from typing import Any

import psutil


def _run(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return ""


def _gpu() -> str:

    output = _run(
        [
            "system_profiler",
            "SPDisplaysDataType",
        ]
    )

    for line in output.splitlines():
        if "Chipset Model:" in line:
            return line.split(":", 1)[1].strip()

    return "Unknown GPU"


def _storage():

    usage = psutil.disk_usage("/")

    gb = 1024 ** 3

    return (
        round(usage.total / gb, 2),
        round(usage.free / gb, 2),
    )


def get_macos_info() -> dict[str, Any]:

    ram = psutil.virtual_memory()

    total, free = _storage()

    return {
        "os": "macOS",
        "os_version": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "cpu": platform.processor() or "Apple Silicon",
        "cpu_cores": psutil.cpu_count(False),
        "cpu_threads": psutil.cpu_count(True),
        "ram_total_gb": round(ram.total / (1024 ** 3), 2),
        "gpu": _gpu(),
        "storage_total_gb": total,
        "storage_free_gb": free,
        "python_version": sys.version.split()[0],
    }