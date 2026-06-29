"""
Base LLM Provider interface (EP-08).
All providers must implement this interface. The rest of the platform never
depends on a concrete vendor implementation.
"""
from abc import ABC, abstractmethod
from typing import Optional
from modules.ai_platform.models import LLMResponse, LLMGenerationOptions


class BaseLLMProvider(ABC):
    """
    Abstract base for all LLM providers.
    Providers: Ollama, OpenAI, Azure OpenAI, Gemini, Claude, etc.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier (e.g. 'ollama', 'openai')."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model to use when none is specified in the request."""
        ...

    @abstractmethod
    async def generate(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[LLMGenerationOptions] = None
    ) -> LLMResponse:
        """
        Send a prompt to the LLM and return a structured LLMResponse.
        Must NOT raise on empty context — return a safe, low-confidence response.
        """
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Health-check whether this provider is reachable."""
        ...
