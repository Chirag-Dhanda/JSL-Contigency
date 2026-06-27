from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class AIRequestPayload(BaseModel):
    user_id: str
    query: str
    current_url: Optional[str] = None
    module_context_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ResponseMetadata(BaseModel):
    latency_ms: int
    model_used: str
    persona_used: str
    tokens_used: int
    timestamp: datetime

class AIStandardResponse(BaseModel):
    answer: str
    referenced_module_id: Optional[str] = None
    referenced_lesson_id: Optional[str] = None
    suggested_next_steps: List[str] = []
    related_resource_ids: List[str] = []
    metadata: ResponseMetadata
