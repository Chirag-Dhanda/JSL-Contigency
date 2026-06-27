import logging
from typing import Dict, Any, List

logger = logging.getLogger("PromptTester")

class PromptTester:
    """Sandbox environment for previewing prompt outputs."""
    
    def __init__(self):
        pass

    def preview_prompt(self, template: str, mock_context: Dict[str, str]) -> str:
        """Injects mock variables to see exactly what the AI will read."""
        from modules.prompt_studio.variables import VariableInjector # inline to avoid circular dep if refactored
        injector = VariableInjector()
        
        logger.info("Generating prompt preview...")
        return injector.inject(template, mock_context)
