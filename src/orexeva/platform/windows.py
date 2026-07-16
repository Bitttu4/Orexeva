"""
Windows platform detection.

Provides detailed system information for Windows machines.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from typing import Any

import psutil


def _run_powershell(command: str) -> str:
    """
    Execute a PowerShell command and return stdout.

    Returns an empty string if the command fails.
    """

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return ""


def _get_cpu_name() -> str:
    """
    Returns the full CPU model name.
    """

    cpu = _run_powershell(
        "(Get-CimInstance Win32_Processor).Name"
    )

    if cpu:
        return cpu.strip()

    cpu = platform.processor()

    if cpu:
        return cpu

    cpu = platform.uname().processor

    if cpu:
        return cpu

    return "Unknown CPU"

def _get_gpu_name() -> str:
    """
    Returns GPU model.
    """

    gpu = _run_powershell(
        "(Get-CimInstance Win32_VideoController).Name"
    )

    if gpu:
        lines = [
            x.strip()
            for x in gpu.splitlines()
            if x.strip()
        ]

        ignore =(
            "Microsoft",
            "remote",
            "IDDCX",
            "Basic Display",
        )

        gpus = []

        for gpu in lines:
            if any(x.lower() in gpu.lower() for x in ignore):
                continue

            gpus.append(gpu)

    return ", ".join(gpus) if gpus else "Unknown GPU"


def _get_storage() -> tuple[float, float]:
    """
    Returns:
        (total_gb, free_gb)
    """

    total = 0
    free = 0

    try:
        partitions = psutil.disk_partitions()

        visited = set()

        for part in partitions:

            if part.device in visited:
                continue

            visited.add(part.device)

            try:
                usage = psutil.disk_usage(part.mountpoint)

                total += usage.total
                free += usage.free

            except PermissionError:
                continue

    except Exception:
        pass

    gb = 1024 ** 3

    return (
        round(total / gb, 2),
        round(free / gb, 2),
    )


def get_windows_info() -> dict[str, Any]:
    """
    Collect Windows system information.
    """

    ram = psutil.virtual_memory()

    total_storage, free_storage = _get_storage()

    return {
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "cpu": _get_cpu_name(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "ram_total_gb": round(ram.total / (1024 ** 3), 2),
        "gpu": _get_gpu_name(),
        "storage_total_gb": total_storage,
        "storage_free_gb": free_storage,
        "python_version": sys.version.split()[0],
    }