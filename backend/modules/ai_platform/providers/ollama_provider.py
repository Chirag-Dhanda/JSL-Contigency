"""
Ollama Provider (EP-08).
Wraps the existing modules/ai/client.py into the BaseLLMProvider interface.
"""
import logging
import time
from typing import Optional, Dict, Any

from modules.ai.client import OllamaClient
from modules.ai.config import ai_config
from modules.ai_platform.models import LLMResponse, LLMGenerationOptions
from .base_provider import BaseLLMProvider

logger = logging.getLogger("AIProvider.Ollama")


class OllamaProvider(BaseLLMProvider):
    """
    Concrete provider implementation wrapping the existing OllamaClient.
    """

    def __init__(self, client: OllamaClient):
        self._client = client

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def default_model(self) -> str:
        return ai_config.default_model

    async def generate(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[LLMGenerationOptions] = None
    ) -> LLMResponse:
        opts = options or LLMGenerationOptions()
        model = opts.model or self.default_model

        t_start = time.monotonic()

        try:
            raw_result = await self._client.generate(
                model=model,
                prompt=user_prompt,
                system=system_prompt,
                stream=False
            )
            latency_ms = (time.monotonic() - t_start) * 1000
            # When stream=False, generate() returns a Dict (not AsyncGenerator)
            raw: Dict[str, Any] = raw_result  # type: ignore[assignment]
            text = raw.get("response", "")
            total_tokens = raw.get("eval_count", 0) + raw.get("prompt_eval_count", 0)

            return LLMResponse(
                provider=self.provider_name,
                model=model,
                raw_text=text,
                total_tokens=total_tokens,
                prompt_tokens=raw.get("prompt_eval_count", 0),
                completion_tokens=raw.get("eval_count", 0),
                latency_ms=round(latency_ms, 2)
            )
        except Exception as e:
            latency_ms = (time.monotonic() - t_start) * 1000
            logger.warning(f"Ollama generation failed: {e}")
            return LLMResponse(
                provider=self.provider_name,
                model=model,
                raw_text="",
                latency_ms=round(latency_ms, 2)
            )

    async def is_available(self) -> bool:
        try:
            models = await self._client.get_models()
            return isinstance(models, list)
        except Exception:
            return False
