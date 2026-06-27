import httpx
import logging
import json
from typing import Dict, Any, Optional, List, AsyncGenerator

from .config import ai_config
from .connection import connection_manager

logger = logging.getLogger("OllamaClient")

class OllamaClient:
    async def generate(self, model: str, prompt: str, system: Optional[str] = None, stream: bool = False) -> Dict[str, Any] | AsyncGenerator[Dict[str, Any], None]:
        """Sends a generation request to the Ollama API with retry logic."""
        endpoint = "/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": ai_config.temperature,
                "top_p": ai_config.top_p,
                "num_ctx": ai_config.context_length
            }
        }
        
        if system:
            payload["system"] = system

        logger.debug(f"Sending AI request to {model}")
        
        if stream:
            return self._generate_stream(endpoint, payload)
        
        response = await connection_manager.request_with_retry("POST", endpoint, json=payload)
        return response.json()

    async def _generate_stream(self, endpoint: str, payload: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        client = await connection_manager.get_client()
        url = f"{connection_manager.base_url}{endpoint}"
        
        async with client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    yield json.loads(line)
                    
    async def get_models(self) -> List[Dict[str, Any]]:
        """Fetches available models from Ollama."""
        endpoint = "/api/tags"
        response = await connection_manager.request_with_retry("GET", endpoint)
        return response.json().get("models", [])
        
    async def check_model_status(self, model: str) -> bool:
        """Checks if a model is available."""
        models = await self.get_models()
        return any(m.get("name") == model or m.get("model") == model for m in models)
