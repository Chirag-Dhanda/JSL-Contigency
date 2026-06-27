import logging
from typing import Dict
from .models import PromptTemplate, PromptStatus

logger = logging.getLogger("PromptDeployer")

class PromptDeployer:
    """Activates and rolls back prompt versions in production."""
    
    def __init__(self):
        # mock active directory: name -> active PromptTemplate
        self._active_prompts: Dict[str, PromptTemplate] = {}

    def deploy_prompt(self, prompt: PromptTemplate) -> bool:
        if prompt.status != PromptStatus.PUBLISHED:
            logger.error(f"Cannot deploy prompt {prompt.prompt_id}. Must be PUBLISHED status.")
            return False
            
        logger.info(f"Deploying prompt {prompt.name} version {prompt.version} to production.")
        self._active_prompts[prompt.name] = prompt
        return True

    def get_active_prompt(self, name: str) -> PromptTemplate:
        return self._active_prompts.get(name)
