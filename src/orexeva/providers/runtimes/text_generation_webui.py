"""
Text Generation WebUI runtime provider.
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

TEXT_GENERATION_WEBUI_EXECUTABLES = ("text-generation-webui", "server.py")
DEFAULT_TIMEOUT = 5


class TextGenerationWebUIProvider(RuntimeProvider):
    """Runtime provider implementation for Text Generation WebUI."""

    _METADATA = ProviderMetadata(
        name="text_generation_webui",
        display_name="Text Generation WebUI",
        category=ProviderCategory.RUNTIME,
        website="https://github.com/oobabooga/text-generation-webui",
        description="Local text generation web UI runtime.",
        supported_platforms=("windows", "linux", "darwin"),
        capabilities=frozenset(),
        tags=("local-ai", "runtime", "webui", "oobabooga"),
    )

    def __init__(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    @property
    def metadata(self) -> ProviderMetadata:
        return self._METADATA

    def _executable(self) -> str | None:
        for candidate in TEXT_GENERATION_WEBUI_EXECUTABLES:
            path = shutil.which(candidate)
            if path is not None:
                return path
        return None

    def _require_executable(self) -> str:
        executable = self._executable()
        if executable is None:
            raise ProviderDetectionError(
                "Text Generation WebUI executable was not found."
            )
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
            raise ProviderDetectionError(
                "Text Generation WebUI executable was not found."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise ProviderRuntimeError(
                "Text Generation WebUI version check timed out."
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise ProviderDetectionError(
                "Failed to determine the installed Text Generation WebUI version."
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
            "Text Generation WebUI installation is handled outside the runtime provider."
        )

    def update(self) -> bool:
        raise ProviderUpdateError(
            "Text Generation WebUI updates are handled outside the runtime provider."
        )

    def uninstall(self) -> bool:
        raise ProviderUninstallError(
            "Text Generation WebUI removal is handled outside the runtime provider."
        )

    def start(self) -> bool:
        raise ProviderRuntimeError(
            "Text Generation WebUI runtime start is not managed by Orexeva."
        )

    def stop(self) -> bool:
        raise ProviderRuntimeError(
            "Text Generation WebUI runtime stop is not managed by Orexeva."
        )

    def status(self) -> ProviderStatus:
        if not self.detect():
            return ProviderStatus.NOT_INSTALLED
        return ProviderStatus.INSTALLED

    def health_check(self) -> bool:
        return self.detect()

    def list_models(self) -> list[dict[str, object]]:
        raise ProviderRuntimeError(
            "Text Generation WebUI model listing is not implemented by Orexeva."
        )

    def pull_model(self, model: str) -> bool:
        raise ProviderRuntimeError(
            f"Text Generation WebUI does not support pulling model '{model}' through Orexeva."
        )

    def remove_model(self, model: str) -> bool:
        raise ProviderRuntimeError(
            f"Text Generation WebUI does not support removing model '{model}' through Orexeva."
        )

    def run_model(self, model: str, prompt: str, **kwargs: object) -> object:
        raise ProviderRuntimeError(
            f"Text Generation WebUI inference for model '{model}' is not implemented by Orexeva."
        )

