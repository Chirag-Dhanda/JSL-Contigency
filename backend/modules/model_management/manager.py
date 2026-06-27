import logging
from typing import List, Dict, Any, Optional

from modules.ai.client import OllamaClient
from modules.ai.config import ai_config

logger = logging.getLogger("ModelManager")

class ModelManager:
    def __init__(self):
        self.client = OllamaClient()
        self.default_model = ai_config.default_model
        self.preferred_model: Optional[str] = None
        self._available_models_cache: List[Dict[str, Any]] = []

    async def get_available_models(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Fetch all available models, using cache unless forced."""
        if not self._available_models_cache or force_refresh:
            try:
                self._available_models_cache = await self.client.get_models()
                logger.info(f"Loaded {len(self._available_models_cache)} models from Ollama.")
            except Exception as e:
                logger.error(f"Failed to fetch models: {e}")
        return self._available_models_cache

    async def get_model_metadata(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific model."""
        models = await self.get_available_models()
        for m in models:
            if m.get("name") == model_name or m.get("model") == model_name:
                return m
        return None

    def set_preferred_model(self, model_name: str) -> None:
        """Set the preferred model for current session/user."""
        self.preferred_model = model_name
        logger.info(f"Preferred model set to {model_name}")

    async def get_active_model(self) -> str:
        """Determine which model to use based on preferences and availability."""
        if self.preferred_model and await self.client.check_model_status(self.preferred_model):
            return self.preferred_model
            
        if await self.client.check_model_status(self.default_model):
            return self.default_model
            
        # Fallback to the first available model if default is not available
        models = await self.get_available_models()
        if models:
            fallback = models[0].get("name")
            logger.warning(f"Default model {self.default_model} not found, falling back to {fallback}")
            return fallback
            
        raise RuntimeError("No AI models available.")

    async def detect_capabilities(self, model_name: str) -> Dict[str, Any]:
        """Detect model capabilities based on model name and metadata."""
        metadata = await self.get_model_metadata(model_name)
        if not metadata:
            return {"vision": False, "tools": False, "context_length": ai_config.context_length}
            
        # Basic capability detection based on model name heuristics (future: read from advanced metadata)
        name = metadata.get("name", "").lower()
        
        return {
            "vision": "llava" in name or "vision" in name,
            "tools": "qwen" in name or "llama3" in name or "tool" in name,
            "context_length": ai_config.context_length,
            "family": metadata.get("details", {}).get("family", "unknown")
        }

model_manager = ModelManager()
