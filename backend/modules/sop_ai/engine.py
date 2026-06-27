import logging
from typing import Dict, Any

from .models import SOPAIResponse
from .navigation import SectionNavigator
from .knowledge_linker import KnowledgeLinker
from modules.procedure_assistant.safety_validator import SafetyValidator

logger = logging.getLogger("SOPAIEngine")

class SOPAIEngine:
    """The central orchestrator for answering SOP and procedure questions."""
    
    def __init__(self):
        self.navigator = SectionNavigator()
        self.linker = KnowledgeLinker()
        self.safety_validator = SafetyValidator()

    def process_query(self, query: str, sop_id: str) -> SOPAIResponse:
        """
        Coordinates the SOP retrieval, ensures safety compliance, and builds the response.
        """
        logger.info(f"Processing SOP query for {sop_id}: '{query}'")
        
        # 1. Navigation
        target_section = self.navigator.locate_section(query)
        logger.debug(f"Target Section Identified: {target_section}")
        
        # 2. Knowledge Linking
        links = self.linker.retrieve_links(sop_id)
        
        # 3. AI Generation (Mocked)
        draft_answer = f"Based on the {target_section or 'General'} section, you should ensure the power is cut before proceeding."
        
        # 4. Safety Validation Middleware (Critical)
        validation = self.safety_validator.validate_response(sop_id, target_section, draft_answer)
        if not validation["is_safe"]:
            logger.warning("Safety Validator caught a potential omission. Injecting mandatory warnings.")
            
        # 5. Build strict response
        return SOPAIResponse(
            answer=draft_answer,
            referenced_sop=sop_id,
            referenced_section=target_section,
            mandatory_safety_notices=validation["mandatory_notices"],
            required_ppe=validation["required_ppe"],
            related_equipment=links["equipment"],
            related_lessons=links["lessons"],
            confidence=0.95
        )
