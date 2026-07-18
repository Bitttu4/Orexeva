"""
Ollama Runtime Provider

Handles detection, installation, verification, runtime control,
and model management for Ollama.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final


# ==========================================================
# Provider Metadata
# ==========================================================


@dataclass(frozen=True, slots=True)
class ProviderMetadata:
    """Immutable metadata describing the provider."""

    name: str
    display_name: str
    category: str
    website: str
    license: str
    supports_windows: bool
    supports_linux: bool
    supports_macos: bool
    supports_cpu: bool
    supports_cuda: bool
    supports_rocm: bool
    supports_metal: bool


METADATA: Final = ProviderMetadata(
    name="ollama",
    display_name="Ollama",
    category="runtime",
    website="https://ollama.com",
    license="MIT",
    supports_windows=True,
    supports_linux=True,
    supports_macos=True,
    supports_cpu=True,
    supports_cuda=True,
    supports_rocm=True,
    supports_metal=True,
)


# ==========================================================
# Platform Commands
# ==========================================================

WINDOWS_INSTALL: Final = [
    "winget",
    "install",
    "--id",
    "Ollama.Ollama",
    "-e",
]

MACOS_INSTALL: Final = [
    "brew",
    "install",
    "ollama",
]

LINUX_INSTALL_SCRIPT: Final = (
    "curl -fsSL https://ollama.com/install.sh | sh"
)

VERSION_COMMAND: Final = [
    "ollama",
    "--version",
]

LIST_MODELS_COMMAND: Final = [
    "ollama",
    "list",
]

PULL_MODEL_COMMAND: Final = [
    "ollama",
    "pull",
]

REMOVE_MODEL_COMMAND: Final = [
    "ollama",
    "rm",
]

RUN_MODEL_COMMAND: Final = [
    "ollama",
    "run",
]

START_SERVER_COMMAND: Final = [
    "ollama",
    "serve",
]


# ==========================================================
# Provider
# ==========================================================


class OllamaProvider:
    """Production-ready Ollama provider."""

    metadata = METADATA

    # ------------------------------------------------------
    # Detection
    # ------------------------------------------------------

    def is_installed(self) -> bool:
        raise NotImplementedError

    def verify(self) -> bool:
        raise NotImplementedError

    def get_version(self) -> str:
        raise NotImplementedError

    # ------------------------------------------------------
    # Installation
    # ------------------------------------------------------

    def install(self) -> bool:
        raise NotImplementedError

    def update(self) -> bool:
        raise NotImplementedError

    def uninstall(self) -> bool:
        raise NotImplementedError

    # ------------------------------------------------------
    # Runtime
    # ------------------------------------------------------

    def start(self) -> bool:
        raise NotImplementedError

    def stop(self) -> bool:
        raise NotImplementedError

    def status(self) -> str:
        raise NotImplementedError

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------

    def list_models(self) -> list[str]:
        raise NotImplementedError

    def pull_model(self, model: str) -> bool:
        raise NotImplementedError

    def remove_model(self, model: str) -> bool:
        raise NotImplementedError

    def run_model(self, model: str) -> bool:
        raise NotImplementedError

    # ------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------

    def _run_command(self, command: list[str]):
        raise NotImplementedError

    def _find_executable(self) -> Path | None:
        raise NotImplementedError