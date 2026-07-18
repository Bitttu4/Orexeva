"""
Provider Exceptions

Custom exceptions used by the Orexeva provider system.
"""


class ProviderError(Exception):
    """Base exception for all provider-related errors."""


class ProviderNotFoundError(ProviderError):
    """Raised when a provider cannot be found."""


class ProviderInstallError(ProviderError):
    """Raised when provider installation fails."""


class ProviderDetectionError(ProviderError):
    """Raised when provider detection fails."""


class ProviderVerificationError(ProviderError):
    """Raised when provider verification fails."""


class ProviderRuntimeError(ProviderError):
    """Raised when runtime operations fail."""


class ProviderUpdateError(ProviderError):
    """Raised when provider update fails."""


class ProviderUninstallError(ProviderError):
    """Raised when provider uninstall fails."""


class UnsupportedPlatformError(ProviderError):
    """Raised when the current platform is not supported."""


class UnsupportedFeatureError(ProviderError):
    """Raised when a provider does not support a requested feature."""