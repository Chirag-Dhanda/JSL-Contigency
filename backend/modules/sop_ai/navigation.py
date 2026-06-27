import logging
from typing import Optional

logger = logging.getLogger("SectionNavigator")

class SectionNavigator:
    """Parses user intent to jump to structural sections of an SOP."""
    
    def __init__(self):
        pass

    def locate_section(self, query: str) -> Optional[str]:
        """
        Determines the target section based on the query.
        Returns the section name or None.
        """
        query_lower = query.lower()
        
        if "safety" in query_lower or "ppe" in query_lower or "hazard" in query_lower:
            return "Safety Rules & PPE"
        elif "quality" in query_lower or "inspection" in query_lower:
            return "Quality Checks"
        elif "startup" in query_lower or "start up" in query_lower:
            return "Startup Procedure"
        elif "shutdown" in query_lower or "shut down" in query_lower:
            return "Shutdown Procedure"
        elif "responsibilities" in query_lower or "who" in query_lower:
            return "Roles & Responsibilities"
            
        return None
