"""
LM Studio runtime provider.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from urllib.error import URLError

from orexeva.providers.base import (
    ProviderCapability,
    ProviderCategory,
    ProviderMetadata,
    ProviderStatus,
    RuntimeProvider,
)
from orexeva.providers.exceptions import (
    ProviderDetectionError,
    ProviderInstallError,
    ProviderRuntimeError,
    ProviderUninstallError,
    ProviderUpdateError,
)

LMSTUDIO_EXECUTABLES = ("lmstudio", "lm-studio")
DEFAULT_TIMEOUT = 5


@dataclass(slots=True)
class _RuntimeProcess:
    """Tracks a runtime process started by Orexeva."""

    process: subprocess.Popen[str]


class LMStudioProvider(RuntimeProvider):
    """Runtime provider implementation for LM Studio."""

    _METADATA = ProviderMetadata(
        name="lmstudio",
        display_name="LM Studio",
        category=ProviderCategory.RUNTIME,
        website="https://lmstudio.ai",
        description="Local model runtime and desktop application.",
        supported_platforms=("windows", "linux", "darwin"),
        capabilities=frozenset(),
        tags=("local-ai", "runtime", "desktop", "lm-studio"),
    )

    def __init__(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout
        self._process: _RuntimeProcess | None = None

    @property
    def metadata(self) -> ProviderMetadata:
        """Provider metadata."""
        return self._METADATA

    def _executable(self) -> str | None:
        for candidate in LMSTUDIO_EXECUTABLES:
            path = shutil.which(candidate)
            if path is not None:
                return path
        return None

    def _require_executable(self) -> str:
        executable = self._executable()
        if executable is None:
            raise ProviderDetectionError("LM Studio executable was not found.")
        return executable

    def detect(self) -> bool:
        """Return True when LM Studio is installed."""
        return self._executable() is not None

    def executable_path(self) -> str | None:
        """Return the detected executable path."""
        return self._executable()

    def version(self) -> str:
        """Return the installed version."""
        executable = self._require_executable()
        try:
            result = subprocess.run(
                [executable, "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=self.timeout,
            )
        except FileNotFoundError as exc:
            raise ProviderDetectionError("LM Studio executable was not found.") from exc
        except subprocess.TimeoutExpired as exc:
            raise ProviderRuntimeError("LM Studio version check timed out.") from exc
        except subprocess.CalledProcessError as exc:
            raise ProviderDetectionError(
                "Failed to determine the installed LM Studio version."
            ) from exc
        return result.stdout.strip() or result.stderr.strip()

    def is_installed(self) -> bool:
        """Return True if LM Studio is installed."""
        return self.detect()

    def verify(self) -> bool:
        """Verify the provider installation."""
        return self.detect()

    def get_version(self) -> str:
        """Return the installed version."""
        return self.version()

    def install(self) -> bool:
        """Install is not managed by the provider layer."""
        raise ProviderInstallError(
            "LM Studio installation is handled outside the runtime provider."
        )

    def uninstall(self) -> bool:
        """Uninstall is not managed by the provider layer."""
        raise ProviderUninstallError(
            "LM Studio removal is handled outside the runtime provider."
        )

    def update(self) -> bool:
        """Update is not managed by the provider layer."""
        raise ProviderUpdateError(
            "LM Studio updates are handled outside the runtime provider."
        )

    def start(self) -> bool:
        """Starting the LM Studio desktop application is unsupported."""
        raise ProviderRuntimeError(
            "LM Studio runtime start is not managed by Orexeva."
        )

    def stop(self) -> bool:
        """Stopping the LM Studio desktop application is unsupported."""
        raise ProviderRuntimeError(
            "LM Studio runtime stop is not managed by Orexeva."
        )

    def status(self) -> ProviderStatus:
        """Return the current provider status."""
        if not self.detect():
            return ProviderStatus.NOT_INSTALLED
        return ProviderStatus.INSTALLED

    def health_check(self) -> bool:
        """Return True when the provider is installed."""
        return self.detect()

    def list_models(self) -> list[dict[str, object]]:
        """List models supported by the provider."""
        raise ProviderRuntimeError(
            "LM Studio model listing is not implemented by Orexeva."
        )

    def pull_model(self, model: str) -> bool:
        """Pulling models is unsupported."""
        raise ProviderRuntimeError(
            f"LM Studio does not support pulling model '{model}' through Orexeva."
        )

    def remove_model(self, model: str) -> bool:
        """Removing models is unsupported."""
        raise ProviderRuntimeError(
            f"LM Studio does not support removing model '{model}' through Orexeva."
        )

    def run_model(self, model: str, prompt: str, **kwargs: object) -> object:
        """Running inference is unsupported in this adapter."""
        raise ProviderRuntimeError(
            f"LM Studio inference for model '{model}' is not implemented by Orexeva."
        )

