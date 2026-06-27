import logging
from typing import Dict, List
from .models import PromptTemplate, PromptStatus

logger = logging.getLogger("PromptVersionManager")

class PromptVersionManager:
    """Manages the version history and state transitions of prompts."""
    
    def __init__(self):
        # Mock storage: prompt_id -> list of versions
        self._prompt_history: Dict[str, List[PromptTemplate]] = {}

    def transition_state(self, prompt: PromptTemplate, new_status: PromptStatus, reviewer_id: str = None) -> PromptTemplate:
        """Transitions a prompt through the lifecycle."""
        logger.info(f"Transitioning {prompt.prompt_id} from {prompt.status} to {new_status}")
        
        prompt.status = new_status
        if new_status == PromptStatus.APPROVED:
            prompt.reviewer = reviewer_id
            
        return prompt
