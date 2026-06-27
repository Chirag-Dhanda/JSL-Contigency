import logging
from typing import List, Optional
from .models import InstalledModel, AIModelConfig

logger = logging.getLogger("AdminModelManager")

class AdminModelManager:
    """Handles configuring and tracking installed AI Models from an admin perspective."""
    
    def __init__(self):
        # In a real system, this pulls from a local DB or config file.
        self._installed_models: List[InstalledModel] = [
            InstalledModel(
                model_id="llama3",
                display_name="Llama 3 8B (Ollama)",
                capabilities=["chat"],
                is_default_chat=True
            ),
            InstalledModel(
                model_id="nomic-embed-text",
                display_name="Nomic Embed",
                capabilities=["embeddings"],
                is_default_embedding=True
            )
        ]

    def get_all_models(self) -> List[InstalledModel]:
        return self._installed_models

    def set_default_chat_model(self, model_id: str) -> bool:
        logger.info(f"Setting default chat model to {model_id}")
        for model in self._installed_models:
            if "chat" in model.capabilities:
                model.is_default_chat = (model.model_id == model_id)
        return True

    def toggle_model(self, model_id: str, enable: bool) -> bool:
        logger.warning(f"Toggling model {model_id} to enable={enable}")
        for model in self._installed_models:
            if model.model_id == model_id:
                model.is_enabled = enable
                return True
        return False
