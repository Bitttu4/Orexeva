"""
Linux platform detection.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from typing import Any

import psutil


def _run_command(command: list[str]) -> str:
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


def _linux_name() -> str:
    try:
        with open("/etc/os-release", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().replace('"', "")
    except Exception:
        pass

    return platform.system()


def _gpu() -> str:
    output = _run_command(["lspci"])

    if output:
        gpus = []

        for line in output.splitlines():
            if (
                "VGA" in line
                or "3D" in line
                or "Display" in line
            ):
                gpus.append(line.split(":")[-1].strip())

        if gpus:
            return ", ".join(gpus)

    return "Unknown GPU"


def _storage() -> tuple[float, float]:
    usage = psutil.disk_usage("/")

    gb = 1024 ** 3

    return (
        round(usage.total / gb, 2),
        round(usage.free / gb, 2),
    )


def get_linux_info() -> dict[str, Any]:

    ram = psutil.virtual_memory()

    total, free = _storage()

    return {
        "os": _linux_name(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "cpu": platform.processor() or "Unknown CPU",
        "cpu_cores": psutil.cpu_count(False),
        "cpu_threads": psutil.cpu_count(True),
        "ram_total_gb": round(ram.total / (1024 ** 3), 2),
        "gpu": _gpu(),
        "storage_total_gb": total,
        "storage_free_gb": free,
        "python_version": sys.version.split()[0],
    }