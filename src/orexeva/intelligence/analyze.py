"""
System analysis stage for Orexeva intelligence.
"""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path
from typing import Any

from orexeva.config import Config
from orexeva.providers import ProviderManager, ProviderStatus

from .types import AnalysisResult, RuntimeInfo, SystemResource


def _normalize_runtimes(provider_manager: ProviderManager) -> tuple[RuntimeInfo, ...]:
    """Build normalized runtime records from the provider layer."""
    runtimes: list[RuntimeInfo] = []
    for name in provider_manager.list_supported():
        provider = provider_manager.get(name)
        metadata = provider.metadata
        status = provider.status() if hasattr(provider, "status") else ProviderStatus.ERROR
        runtimes.append(
            RuntimeInfo(
                name=metadata.name,
                display_name=metadata.display_name,
                status=status,
                version=metadata.version,
                installed=provider.is_installed(),
                supported_platforms=metadata.supported_platforms,
                capabilities=tuple(cap.value for cap in metadata.capabilities),
            )
        )
    return tuple(runtimes)


def _detect_platform_info() -> dict[str, Any]:
    """Detect platform information while tolerating missing optional dependencies."""
    def _fallback() -> dict[str, Any]:
        gb = 1024 ** 3
        cpu_count = os.cpu_count()
        try:
            usage = shutil.disk_usage(Path.home())
            storage_total_gb = round(usage.total / gb, 2)
            storage_free_gb = round(usage.free / gb, 2)
        except Exception:
            storage_total_gb = None
            storage_free_gb = None
        return {
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "cpu": platform.processor() or platform.machine(),
            "cpu_cores": cpu_count,
            "cpu_threads": cpu_count,
            "ram_total_gb": None,
            "storage_total_gb": storage_total_gb,
            "storage_free_gb": storage_free_gb,
            "python_version": platform.python_version(),
        }

    try:
        from orexeva.platform import detect as detect_platform
    except ModuleNotFoundError:
        return _fallback()

    try:
        return detect_platform()
    except Exception:
        return _fallback()


def analyze(
    provider_manager: ProviderManager | None = None,
    config: Config | None = None,
    registry: dict[str, Any] | None = None,
) -> AnalysisResult:
    """Analyze the detected system and normalize the inputs."""
    platform_info = _detect_platform_info()
    manager = provider_manager or ProviderManager()
    if not manager.list_supported():
        manager.discover()

    system = SystemResource(
        cpu=str(platform_info.get("cpu", "")),
        cpu_cores=platform_info.get("cpu_cores"),
        cpu_threads=platform_info.get("cpu_threads"),
        gpu=str(platform_info.get("gpu", "")),
        ram_total_gb=platform_info.get("ram_total_gb"),
        storage_total_gb=platform_info.get("storage_total_gb"),
        storage_free_gb=platform_info.get("storage_free_gb"),
        os=str(platform_info.get("os", "")),
        os_version=str(platform_info.get("os_version", "")),
        architecture=str(platform_info.get("architecture", "")),
        python_version=str(platform_info.get("python_version", "")),
    )

    config_data = config.all() if config is not None else {}
    registry_data = dict(registry) if registry is not None else {}

    return AnalysisResult(
        system=system,
        runtimes=_normalize_runtimes(manager),
        config=config_data,
        registry=registry_data,
    )
