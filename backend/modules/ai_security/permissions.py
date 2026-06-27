import logging
from typing import List

logger = logging.getLogger("AIPermissionManager")

class AIPermissionManager:
    """Enforces Role-Based Access Control specifically for AI modules."""
    
    def __init__(self):
        pass

    def check_access(self, user_role: str, ai_module: str) -> bool:
        """Determines if a role is authorized to use a specific AI agent."""
        logger.debug(f"Checking access for role {user_role} to {ai_module}")
        
        # Mock policy
        restricted_modules = {
            "ManufacturingExpert": ["Operator", "Engineer", "Manager"],
            "HRDataAgent": ["HR", "Manager"]
        }
        
        allowed_roles = restricted_modules.get(ai_module)
        if allowed_roles and user_role not in allowed_roles:
            logger.warning(f"Access Denied: {user_role} attempted to use {ai_module}")
            return False
            
        return True
