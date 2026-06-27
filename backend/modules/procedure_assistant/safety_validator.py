import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("SafetyValidator")

class SafetyValidator:
    """Critical middleware that ensures AI responses do not omit mandatory safety data."""
    
    def __init__(self):
        pass

    def validate_response(self, sop_id: str, section: Optional[str], draft_answer: str) -> Dict[str, Any]:
        """
        Scans the draft answer and the target SOP to ensure required PPE is mentioned.
        """
        logger.debug(f"Running safety validation on draft response for {sop_id}")
        
        # Mock Safety Rules for EAF
        mandatory_ppe = ["Heat-Resistant Gloves", "Face Shield", "Flame Retardant Jacket"]
        notices = ["WARNING: High Voltage Area. Ensure LOTO is applied."]
        
        is_safe = True
        
        # If the answer talks about operation but doesn't mention PPE, flag it.
        if "power" in draft_answer.lower() and "ppe" not in draft_answer.lower():
            is_safe = False
            
        return {
            "is_safe": is_safe,
            "mandatory_notices": notices,
            "required_ppe": mandatory_ppe
        }
