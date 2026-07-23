"""
orexeva.providers.runtimes.ollama

Production implementation of the Ollama runtime provider.

Responsibilities
----------------
- Detect Ollama installation
- Detect executable path
- Retrieve installed version
- Check runtime availability
- Perform runtime health checks

This module MUST NOT:
- Print CLI output
- Contain business logic
- Select providers
- Perform recommendation logic
- Manage configuration
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from subprocess import DEVNULL
from urllib.error import URLError
from urllib.request import Request, urlopen

from orexeva.providers.base import (
    ProviderCapability,
    ProviderCategory,
    ProviderMetadata,
    ProviderStatus,
    RuntimeProvider,
)
from orexeva.providers.exceptions import (
    ProviderDetectionError,
    ProviderHealthError,
    ProviderInstallError,
    ProviderRuntimeError,
    ProviderUninstallError,
    ProviderUpdateError,
)


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

OLLAMA_EXECUTABLE = "ollama"

DEFAULT_HOST = "http://127.0.0.1:11434"

VERSION_ENDPOINT = "/api/version"

TAGS_ENDPOINT = "/api/tags"

PULL_ENDPOINT = "/api/pull"

DELETE_ENDPOINT = "/api/delete"

DEFAULT_TIMEOUT = 5


# ---------------------------------------------------------------------
# Ollama Provider
# ---------------------------------------------------------------------


@dataclass(slots=True)
class _RuntimeProcess:
    """Tracks the runtime process started by Orexeva."""

    process: subprocess.Popen[str]


class OllamaProvider(RuntimeProvider):
    """
    Runtime provider implementation for Ollama.
    """

    metadata = ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        category=ProviderCategory.RUNTIME,
        website="https://ollama.com",
        description="Local AI runtime with an HTTP API for model management.",
        supported_platforms=("windows", "linux", "darwin"),
        capabilities=frozenset(
            {
                ProviderCapability.SERVER,
                ProviderCapability.API,
                ProviderCapability.MODELS,
                ProviderCapability.DOWNLOAD,
                ProviderCapability.UPDATE,
                ProviderCapability.UNINSTALL,
                ProviderCapability.CHAT,
            }
        ),
        tags=("local-ai", "runtime", "llm", "ollama"),
    )

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout
        self._process: _RuntimeProcess | None = None

    def _url(self, endpoint: str) -> str:
        """Returns the complete Ollama API URL."""
        return f"{self.host}{endpoint}"

    # -----------------------------------------------------------------
    # Detection
    # -----------------------------------------------------------------

    def detect(self) -> bool:
        """
        Returns True if the Ollama executable is installed.
        """
        return shutil.which(OLLAMA_EXECUTABLE) is not None

    def executable_path(self) -> str | None:
        """
        Returns the absolute executable path.

        Returns
        -------
        str | None
        """
        return shutil.which(OLLAMA_EXECUTABLE)

    # -----------------------------------------------------------------
    # Version
    # -----------------------------------------------------------------

    def version(self) -> str:
        """
        Returns the installed Ollama version.

        Raises
        ------
        ProviderDetectionError
            If Ollama is not installed.
        """

        if not self.detect():
            raise ProviderDetectionError(
                "Ollama executable was not found."
            )

        try:
            result = subprocess.run(
                [OLLAMA_EXECUTABLE, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            raise ProviderDetectionError(
                "Failed to determine the installed Ollama version."
            ) from exc

    def is_installed(self) -> bool:
        """Return True if Ollama is installed."""
        return self.detect()

    def verify(self) -> bool:
        """Verify that Ollama is installed and reachable."""
        return self.detect() and self.health_check()

    def get_version(self) -> str:
        """Return the installed Ollama version."""
        return self.version()

    # -----------------------------------------------------------------
    # Runtime Status
    # -----------------------------------------------------------------

    def is_running(self) -> bool:
        """
        Returns True if the Ollama runtime is responding.
        """

        try:
            with urlopen(
                self._url(VERSION_ENDPOINT),
                timeout=self.timeout,
            ) as response:
                return response.status == 200

        except URLError:
            return False

    # -----------------------------------------------------------------
    # Health
    # -----------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Performs a runtime health check.

        Returns
        -------
        bool

        Raises
        ------
        ProviderDetectionError
        ProviderHealthError
        """

        if not self.detect():
            raise ProviderDetectionError(
                "Ollama is not installed."
            )

        try:
            with urlopen(
                self._url(TAGS_ENDPOINT),
                timeout=self.timeout,
            ) as response:

                if response.status != 200:
                    raise ProviderHealthError(
                        f"Ollama returned HTTP {response.status}"
                    )

                try:
                    json.loads(response.read())
                except json.JSONDecodeError as exc:
                    raise ProviderHealthError(
                        "Invalid response received from the Ollama runtime."
                    ) from exc

                return True

        except URLError as exc:
            raise ProviderHealthError(
                "Unable to connect to the Ollama runtime."
            ) from exc

    def install(self) -> bool:
        """Install Ollama is not managed by this provider."""
        raise ProviderInstallError(
            "Ollama installation is handled outside the runtime provider."
        )

    def update(self) -> bool:
        """Update Ollama is not managed by this provider."""
        raise ProviderUpdateError(
            "Ollama updates are handled outside the runtime provider."
        )

    def uninstall(self) -> bool:
        """Uninstall Ollama is not managed by this provider."""
        raise ProviderUninstallError(
            "Ollama removal is handled outside the runtime provider."
        )

    # -----------------------------------------------------------------
    # Information
    # -----------------------------------------------------------------

    @property
    def name(self) -> str:
        return "Ollama"

    @property
    def runtime_type(self) -> str:
        return "runtime"

    @property
    def executable(self) -> str:
        return OLLAMA_EXECUTABLE

    def start(self) -> bool:
        """Start the Ollama runtime if it is not already running."""
        if self.is_running():
            return True

        if not self.detect():
            raise ProviderDetectionError("Ollama is not installed.")

        try:
            process = subprocess.Popen(
                [OLLAMA_EXECUTABLE, "serve"],
                stdout=DEVNULL,
                stderr=DEVNULL,
                text=True,
            )
        except OSError as exc:
            raise ProviderRuntimeError(
                "Failed to start the Ollama runtime."
            ) from exc

        self._process = _RuntimeProcess(process=process)
        return True

    def stop(self) -> bool:
        """Stop the Ollama runtime if Orexeva started it."""
        process = self._process

        if process is None:
            return not self.is_running()

        if process.process.poll() is None:
            process.process.terminate()

            try:
                process.process.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                process.process.kill()
                process.process.wait(timeout=self.timeout)

        self._process = None
        return True

    def status(self) -> ProviderStatus:
        """Return the current Ollama runtime status."""
        if not self.detect():
            return ProviderStatus.NOT_INSTALLED

        if self.is_running():
            return ProviderStatus.RUNNING

        return ProviderStatus.STOPPED
    
    # -----------------------------------------------------------------
    # Model Operations
    # -----------------------------------------------------------------

    def list_models(self) -> list[dict[str, object]]:
        """Returns all installed Ollama models."""

        self.health_check()

        try:
            with urlopen(
                self._url(TAGS_ENDPOINT),
                timeout=self.timeout,
            ) as response:
                try:
                    data = json.loads(response.read())
                except json.JSONDecodeError as exc:
                    raise ProviderHealthError(
                        "Invalid response received from the Ollama runtime."
                    ) from exc

                models = data.get("models", [])
                if not isinstance(models, list):
                    raise ProviderHealthError(
                        "Invalid model list received from the Ollama runtime."
                    )

                # Server returns list[dict]
                return models

        except URLError as exc:
            raise ProviderHealthError(
                "Failed to retrieve installed models."
            ) from exc

    def pull_model(self, model: str) -> bool:
        """
        Downloads a model from the Ollama registry.
        """

        self.health_check()

        payload = json.dumps(
            {
                "name": model,
                "stream": False,
            }
        ).encode("utf-8")

        try:
            request = Request(
                self._url(PULL_ENDPOINT),
                data=payload,
                headers={
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:

                return response.status == 200

        except URLError as exc:
            raise ProviderHealthError(
                f"Failed to pull model '{model}'."
            ) from exc

    def remove_model(self, model: str) -> bool:
        """
        Removes an installed model.
        """

        self.health_check()

        payload = json.dumps(
            {
                "name": model,
            }
        ).encode("utf-8")

        try:
            request = Request(
                self._url(DELETE_ENDPOINT),
                data=payload,
                headers={
                    "Content-Type": "application/json",
                },
                method="DELETE",
            )

            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:

                return response.status == 200

        except URLError as exc:
            raise ProviderHealthError(
                f"Failed to remove model '{model}'."
            ) from exc

    def run_model(
        self,
        model: str,
        prompt: str,
        **kwargs: object,
    ) -> object:
        """Run a prompt against a loaded model."""
        self.health_check()

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        payload.update(kwargs)

        try:
            request = Request(
                self._url("/api/generate"),
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urlopen(request, timeout=self.timeout) as response:
                if response.status != 200:
                    raise ProviderRuntimeError(
                        f"Ollama returned HTTP {response.status}"
                    )

                try:
                    return json.loads(response.read())
                except json.JSONDecodeError as exc:
                    raise ProviderRuntimeError(
                        "Invalid generation response received from Ollama."
                    ) from exc

        except URLError as exc:
            raise ProviderRuntimeError(
                f"Failed to run model '{model}'."
            ) from exc

    def model_info(self, model: str) -> dict[str, object]:
        """
        Returns metadata for a specific model.
        """

        models = self.list_models()

        for installed_model in models:

            if installed_model.get("name") == model:
                return installed_model

        raise ProviderHealthError(
            f"Model '{model}' is not installed."
        )

    def model_exists(self, model: str) -> bool:
        """
        Returns True if the specified model is installed.
        """

        try:
            self.model_info(model)
            return True

        except ProviderHealthError:
            return False

    def installed_model_names(self) -> list[str]:
        """
        Returns the names of all installed models.
        """

        return [
            model["name"]
            for model in self.list_models()
            if "name" in model
        ]

    def model_count(self) -> int:
        """
        Returns the number of installed models.
        """

        return len(self.list_models())
