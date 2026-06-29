"""
Provider Registry (EP-08).
Runtime-configurable registry of LLM providers.
"""
import logging
from typing import Dict, Optional
from .base_provider import BaseLLMProvider

logger = logging.getLogger("AIProvider.Registry")


class ProviderRegistry:
    """
    Manages available LLM providers and resolves the active one.
    
    All calls to AI must go through this registry.
    No module may instantiate a provider directly.
    """

    def __init__(self, default_provider: str = "ollama"):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._default = default_provider

    def register(self, provider: BaseLLMProvider) -> None:
        self._providers[provider.provider_name] = provider
        logger.info(f"Registered AI provider: '{provider.provider_name}'")

    def resolve(self, name: Optional[str] = None) -> BaseLLMProvider:
        target = name or self._default
        provider = self._providers.get(target)
        if not provider:
            available = list(self._providers.keys())
            raise ValueError(f"Provider '{target}' not registered. Available: {available}")
        return provider

    def list_providers(self) -> list:
        return list(self._providers.keys())

    def set_default(self, name: str) -> None:
        if name not in self._providers:
            raise ValueError(f"Cannot set default: provider '{name}' not registered.")
        self._default = name
        logger.info(f"Default AI provider set to: '{name}'")


from typing import Optional
