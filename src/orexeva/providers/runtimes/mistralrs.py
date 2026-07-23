"""
Mistral.rs runtime provider.
"""

from __future__ import annotations

import shutil
import subprocess

from orexeva.providers.base import (
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

MISTRALRS_EXECUTABLES = ("mistralrs", "mistralrs-server")
DEFAULT_TIMEOUT = 5


class MistralRsProvider(RuntimeProvider):
    """Runtime provider implementation for Mistral.rs."""

    _METADATA = ProviderMetadata(
        name="mistralrs",
        display_name="Mistral.rs",
        category=ProviderCategory.RUNTIME,
        website="https://github.com/EricLBuehler/mistral.rs",
        description="Local Mistral.rs runtime.",
        supported_platforms=("windows", "linux", "darwin"),
        capabilities=frozenset(),
        tags=("local-ai", "runtime", "mistral.rs"),
    )

    def __init__(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    @property
    def metadata(self) -> ProviderMetadata:
        return self._METADATA

    def _executable(self) -> str | None:
        for candidate in MISTRALRS_EXECUTABLES:
            path = shutil.which(candidate)
            if path is not None:
                return path
        return None

    def _require_executable(self) -> str:
        executable = self._executable()
        if executable is None:
            raise ProviderDetectionError("Mistral.rs executable was not found.")
        return executable

    def detect(self) -> bool:
        return self._executable() is not None

    def executable_path(self) -> str | None:
        return self._executable()

    def version(self) -> str:
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
            raise ProviderDetectionError("Mistral.rs executable was not found.") from exc
        except subprocess.TimeoutExpired as exc:
            raise ProviderRuntimeError("Mistral.rs version check timed out.") from exc
        except subprocess.CalledProcessError as exc:
            raise ProviderDetectionError(
                "Failed to determine the installed Mistral.rs version."
            ) from exc
        return result.stdout.strip() or result.stderr.strip()

    def is_installed(self) -> bool:
        return self.detect()

    def verify(self) -> bool:
        return self.detect()

    def get_version(self) -> str:
        return self.version()

    def install(self) -> bool:
        raise ProviderInstallError(
            "Mistral.rs installation is handled outside the runtime provider."
        )

    def update(self) -> bool:
        raise ProviderUpdateError(
            "Mistral.rs updates are handled outside the runtime provider."
        )

    def uninstall(self) -> bool:
        raise ProviderUninstallError(
            "Mistral.rs removal is handled outside the runtime provider."
        )

    def start(self) -> bool:
        raise ProviderRuntimeError("Mistral.rs runtime start is not managed by Orexeva.")

    def stop(self) -> bool:
        raise ProviderRuntimeError("Mistral.rs runtime stop is not managed by Orexeva.")

    def status(self) -> ProviderStatus:
        if not self.detect():
            return ProviderStatus.NOT_INSTALLED
        return ProviderStatus.INSTALLED

    def health_check(self) -> bool:
        return self.detect()

    def list_models(self) -> list[dict[str, object]]:
        raise ProviderRuntimeError(
            "Mistral.rs model listing is not implemented by Orexeva."
        )

    def pull_model(self, model: str) -> bool:
        raise ProviderRuntimeError(
            f"Mistral.rs does not support pulling model '{model}' through Orexeva."
        )

    def remove_model(self, model: str) -> bool:
        raise ProviderRuntimeError(
            f"Mistral.rs does not support removing model '{model}' through Orexeva."
        )

    def run_model(self, model: str, prompt: str, **kwargs: object) -> object:
        raise ProviderRuntimeError(
            f"Mistral.rs inference for model '{model}' is not implemented by Orexeva."
        )

