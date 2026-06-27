import logging
from typing import Dict, Any
from datetime import datetime, timezone

from .models import AIRequestPayload, AIStandardResponse, ResponseMetadata
from .enums import AITaskType, AIPersona

logger = logging.getLogger("IntelligentRouter")

class IntelligentRouter:
    """Intelligent middleware evaluating the context before hitting the AI Gateway."""
    
    def __init__(self):
        # In a real app, these would be injected
        pass

    def evaluate_persona(self, payload: AIRequestPayload, context: Dict[str, Any]) -> AIPersona:
        """Determines the appropriate persona based on the user's location and query."""
        url = payload.current_url or ""
        
        if "safety" in url.lower() or "hazard" in payload.query.lower():
            return AIPersona.SAFETY_EXPERT
        elif "equipment" in url.lower() or "machine" in payload.query.lower():
            return AIPersona.MANUFACTURING_EXPERT
        elif "sop" in url.lower():
            return AIPersona.GENERAL_ASSISTANT # Could be SOP specific
        
        return AIPersona.GENERAL_ASSISTANT

    def route_request(self, payload: AIRequestPayload) -> AIStandardResponse:
        """
        Main entry point for the frontend.
        1. Gathers context.
        2. Determines persona.
        3. Forwards to Gateway.
        """
        logger.info(f"Routing AI Request from user {payload.user_id}")
        
        # 1. Fetch Context (Mocked for now, handled by ContextManager)
        context = {
            "department": "Unknown",
            "permissions": ["read"]
        }
        
        # 2. Evaluate Persona
        persona = self.evaluate_persona(payload, context)
        logger.debug(f"Selected Persona: {persona.value}")
        
        # 3. Compile final request (Handled heavily by PromptEngine and Gateway)
        # Mocking the gateway response for structural purposes
        
        meta = ResponseMetadata(
            latency_ms=450,
            model_used="llama3:latest",
            persona_used=persona.value,
            tokens_used=120,
            timestamp=datetime.now(timezone.utc)
        )
        
        response = AIStandardResponse(
            answer="This is a standardized response returned by the AI Gateway.",
            metadata=meta
        )
        
        return response

    async def route_copilot_request(self, prompt: str, user_id: str, conv_id: str, context_block: Any) -> AIStandardResponse:
        logger.info(f"Routing Copilot Request from user {user_id}")
        meta = ResponseMetadata(
            latency_ms=450,
            model_used="llama3:latest",
            persona_used="copilot",
            tokens_used=150,
            timestamp=datetime.now(timezone.utc)
        )
        return AIStandardResponse(
            answer=f"Simulated copilot response for: {prompt}",
            metadata=meta
        )

ai_router = IntelligentRouter()
