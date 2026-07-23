"""
Base classes for the Orexeva Provider System.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet


# ==========================================================
# Provider Category
# ==========================================================


class ProviderCategory(str, Enum):
    """Supported provider categories."""

    RUNTIME = "runtime"
    IMAGE = "image"
    AUDIO = "audio"
    CLOUD = "cloud"
    VECTOR = "vector"
    CONTAINER = "container"
    HARDWARE = "hardware"
    SOURCE = "source"


# ==========================================================
# Provider Capability
# ==========================================================


class ProviderCapability(str, Enum):
    """Capabilities supported by a provider."""

    # Hardware
    CPU = "cpu"
    CUDA = "cuda"
    ROCM = "rocm"
    METAL = "metal"

    # Runtime
    SERVER = "server"
    API = "api"
    OPENAI = "openai"

    # Models
    MODELS = "models"
    DOWNLOAD = "download"
    UPDATE = "update"
    UNINSTALL = "uninstall"

    # AI Features
    CHAT = "chat"
    EMBEDDINGS = "embeddings"
    VISION = "vision"
    AUDIO = "audio"

    # Advanced
    STREAMING = "streaming"
    BATCH = "batch"
    MULTIMODAL = "multimodal"


# ==========================================================
# Provider Status
# ==========================================================


class ProviderStatus(str, Enum):
    """Current provider status."""

    NOT_INSTALLED = "not_installed"
    INSTALLING = "installing"
    INSTALLED = "installed"

    RUNNING = "running"
    STOPPED = "stopped"

    UPDATING = "updating"
    ERROR = "error"


# ==========================================================
# Provider Metadata
# ==========================================================


@dataclass(slots=True, frozen=True)
class ProviderMetadata:
    """Immutable provider metadata."""

    name: str
    display_name: str
    category: ProviderCategory

    version: str = ""
    description: str = ""
    website: str = ""
    license: str = ""

    supported_platforms: tuple[str, ...] = ()
    supported_architectures: tuple[str, ...] = ()

    capabilities: FrozenSet[ProviderCapability] = field(
        default_factory=frozenset
    )

    tags: tuple[str, ...] = ()


# ==========================================================
# Base Provider
# ==========================================================


class BaseProvider(ABC):
    """Base class for every Orexeva provider."""

    @property
    @abstractmethod
    def metadata(self) -> ProviderMetadata:
        """Provider metadata."""

    def supports(
        self,
        capability: ProviderCapability,
    ) -> bool:
        """Return True if the provider supports a capability."""
        return capability in self.metadata.capabilities

    @abstractmethod
    def is_installed(self) -> bool:
        """Return True if the provider is installed."""

    @abstractmethod
    def install(self) -> bool:
        """Install the provider."""

    @abstractmethod
    def verify(self) -> bool:
        """Verify the provider installation."""

    @abstractmethod
    def uninstall(self) -> bool:
        """Uninstall the provider."""

    @abstractmethod
    def update(self) -> bool:
        """Update the provider."""

    @abstractmethod
    def get_version(self) -> str:
        """Return the installed version."""


# ==========================================================
# Runtime Provider
# ==========================================================


class RuntimeProvider(BaseProvider):
    """Base class for local inference runtimes."""

    @abstractmethod
    def start(self) -> bool:
        """Start the runtime."""

    @abstractmethod
    def stop(self) -> bool:
        """Stop the runtime."""

    @abstractmethod
    def status(self) -> ProviderStatus:
        """Return current runtime status."""

    @abstractmethod
    def list_models(self) -> list[dict[str, Any]]:
        """Return installed models."""

    @abstractmethod
    def pull_model(self, model: str) -> bool:
        """Download a model."""

    @abstractmethod
    def remove_model(self, model: str) -> bool:
        """Remove a model."""

    @abstractmethod
    def run_model(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> Any:
        """Run inference."""
