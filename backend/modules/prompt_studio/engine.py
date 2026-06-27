import logging
from typing import Dict, Any, List

from modules.prompts.models import PromptTemplate
from modules.prompts.versioning import PromptVersionManager
from modules.prompts.deployment import PromptDeployer
from modules.prompts.governance import PromptGovernance

logger = logging.getLogger("PromptStudioEngine")

class PromptStudioEngine:
    """The central orchestrator for the Prompt Studio UI."""
    
    def __init__(self):
        self.versioning = PromptVersionManager()
        self.deployer = PromptDeployer()
        self.governance = PromptGovernance()

    def create_draft(self, prompt_data: Dict[str, Any]) -> PromptTemplate:
        """Generates a new Draft prompt."""
        logger.info(f"Creating new draft prompt: {prompt_data.get('name')}")
        
        template = PromptTemplate(
            prompt_id=prompt_data["prompt_id"],
            name=prompt_data["name"],
            category=prompt_data["category"],
            description=prompt_data["description"],
            system_prompt=prompt_data["system_prompt"],
            prompt_body=prompt_data["prompt_body"],
            author=prompt_data["author"]
        )
        return template
