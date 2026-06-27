import logging
from .models import PromptTemplate, PromptStatus

logger = logging.getLogger("PromptGovernance")

class PromptGovernance:
    """Enforces approval workflows and permission rules."""
    
    def __init__(self):
        pass

    def request_approval(self, prompt: PromptTemplate) -> bool:
        """Submits a draft prompt for review."""
        if prompt.status != PromptStatus.DRAFT:
            return False
            
        logger.info(f"Prompt {prompt.prompt_id} submitted for review.")
        prompt.status = PromptStatus.REVIEW
        return True
