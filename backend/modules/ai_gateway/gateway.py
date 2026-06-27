import logging
import time
from typing import Dict, Any
from datetime import datetime, timezone

from modules.ai_router.models import AIRequestPayload, AIStandardResponse, ResponseMetadata
from modules.ai_router.enums import AIPersona
from modules.ai.client import OllamaClient
from modules.prompts.engine import PromptEngine
from modules.model_management.manager import ModelManager

logger = logging.getLogger("EnterpriseAIGateway")

class EnterpriseAIGateway:
    """The central gatekeeper for all AI requests. Enforces permissions and audits calls."""
    
    def __init__(self):
        self.client = OllamaClient()
        self.prompt_engine = PromptEngine()
        self.model_manager = ModelManager()

    def _check_permissions(self, payload: AIRequestPayload, context: Dict[str, Any]) -> bool:
        """Verifies the user has permission to ask questions about the current context."""
        # E.g., if context["department"] == "IT" but user permissions don't allow IT access
        return True # Mock pass

    def _audit_log(self, payload: AIRequestPayload, meta: ResponseMetadata):
        """Persists the AI interaction to the audit log."""
        logger.info(
            f"AUDIT | User: {payload.user_id} | Persona: {meta.persona_used} | "
            f"Model: {meta.model_used} | Latency: {meta.latency_ms}ms | Tokens: {meta.tokens_used}"
        )

    async def execute_request(self, 
                              payload: AIRequestPayload, 
                              context: Dict[str, Any], 
                              persona: AIPersona) -> AIStandardResponse:
        """Executes the fully formatted request against the AI Client."""
        
        start_time = time.time()
        
        if not self._check_permissions(payload, context):
            raise PermissionError("User does not have access to this context.")
            
        # 1. Compile prompt
        system_prompt = self.prompt_engine.get_system_prompt()
        final_prompt = self.prompt_engine.compile_prompt(payload.query, context, persona.value)
        
        # 2. Get Model
        model = self.model_manager.get_preferred_model()
        
        # 3. Call AI
        try:
            raw_response = await self.client.generate(
                model=model,
                prompt=final_prompt,
                system=system_prompt
            )
            answer_text = raw_response.get("response", "Error generating response.")
            # For simplicity, estimating tokens if Ollama doesn't return eval_count
            tokens = raw_response.get("eval_count", len(answer_text.split())) 
        except Exception as e:
            logger.error(f"AI Generation Failed: {e}")
            answer_text = "I am currently unable to reach the knowledge engine. Please try again later."
            tokens = 0
            
        latency = int((time.time() - start_time) * 1000)
        
        # 4. Standardize Response
        meta = ResponseMetadata(
            latency_ms=latency,
            model_used=model,
            persona_used=persona.value,
            tokens_used=tokens,
            timestamp=datetime.now(timezone.utc)
        )
        
        response = AIStandardResponse(
            answer=answer_text,
            metadata=meta
        )
        
        # 5. Audit
        self._audit_log(payload, meta)
        
        return response
