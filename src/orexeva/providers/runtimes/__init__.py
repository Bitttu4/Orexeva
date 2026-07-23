"""Built-in runtime provider implementations."""

from __future__ import annotations

from .jan import JanProvider
from .koboldcpp import KoboldCppProvider
from .llamacpp import LlamaCppProvider
from .lmstudio import LMStudioProvider
from .mistralrs import MistralRsProvider
from .ollama import OllamaProvider
from .text_generation_webui import TextGenerationWebUIProvider
from .vllm import VLLMProvider

PROVIDER_TYPES = (
    OllamaProvider,
    LMStudioProvider,
    LlamaCppProvider,
    JanProvider,
    KoboldCppProvider,
    MistralRsProvider,
    TextGenerationWebUIProvider,
    VLLMProvider,
)
