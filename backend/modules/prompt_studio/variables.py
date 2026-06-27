import logging
from typing import Dict
import re

logger = logging.getLogger("VariableInjector")

class VariableInjector:
    """Safely injects dynamic variables into prompt templates."""
    
    def __init__(self):
        pass

    def inject(self, template: str, context: Dict[str, str]) -> str:
        """Replaces standard variables e.g., {current_user} with context values."""
        logger.debug("Injecting variables into prompt")
        
        result = template
        for var, val in context.items():
            pattern = r"\{" + var + r"\}"
            result = re.sub(pattern, str(val), result)
            
        return result
