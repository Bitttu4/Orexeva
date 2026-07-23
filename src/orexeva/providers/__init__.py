"""Orexeva provider layer."""

from __future__ import annotations

from .base import (
    BaseProvider,
    ProviderCapability,
    ProviderCategory,
    ProviderMetadata,
    ProviderStatus,
    RuntimeProvider,
)
from .catalog import (
    clear_catalog,
    get_metadata,
    get_provider,
    list_by_category,
    list_metadata,
    list_providers,
    provider_count,
    provider_exists,
    register_provider,
    unregister_provider,
)
from .exceptions import (
    ProviderAlreadyRegisteredError,
    ProviderDetectionError,
    ProviderError,
    ProviderHealthError,
    ProviderInstallError,
    ProviderNotFoundError,
    ProviderRuntimeError,
    ProviderUninstallError,
    ProviderUpdateError,
    ProviderVerificationError,
    UnsupportedFeatureError,
    UnsupportedPlatformError,
)
from .manager import ProviderManager
from .runtimes import PROVIDER_TYPES
from .runtimes import (
    JanProvider,
    KoboldCppProvider,
    LlamaCppProvider,
    LMStudioProvider,
    MistralRsProvider,
    OllamaProvider,
    TextGenerationWebUIProvider,
    VLLMProvider,
)

for provider_type in PROVIDER_TYPES:
    try:
        register_provider(provider_type)
    except ProviderAlreadyRegisteredError:
        pass

__all__ = [
    "BaseProvider",
    "ProviderCapability",
    "ProviderCategory",
    "ProviderMetadata",
    "ProviderStatus",
    "RuntimeProvider",
    "ProviderAlreadyRegisteredError",
    "ProviderDetectionError",
    "ProviderError",
    "ProviderHealthError",
    "ProviderInstallError",
    "ProviderNotFoundError",
    "ProviderRuntimeError",
    "ProviderUninstallError",
    "ProviderUpdateError",
    "ProviderVerificationError",
    "UnsupportedFeatureError",
    "UnsupportedPlatformError",
    "ProviderManager",
    "PROVIDER_TYPES",
    "JanProvider",
    "KoboldCppProvider",
    "LlamaCppProvider",
    "LMStudioProvider",
    "MistralRsProvider",
    "OllamaProvider",
    "TextGenerationWebUIProvider",
    "VLLMProvider",
    "clear_catalog",
    "get_metadata",
    "get_provider",
    "list_by_category",
    "list_metadata",
    "list_providers",
    "provider_count",
    "provider_exists",
    "register_provider",
    "unregister_provider",
]
