import logging
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from exceptions.base import NotFoundException

logger = logging.getLogger("AIReviewQueue")

class AIReviewSuggestion(BaseModel):
    """
    Represents an AI-generated suggestion that requires MASTER_EDITOR approval.
    """
    id: str = Field(default_factory=lambda: f"sug-{uuid.uuid4().hex[:8]}")
    suggestion_type: str = Field(..., description="'LESSON_GENERATION', 'SUMMARY', 'RELATIONSHIP_LINK'")
    target_entity_id: Optional[str] = None
    ai_confidence: float = Field(..., description="0.0 to 1.0 score")
    payload: Dict[str, Any] = Field(..., description="The suggested changes or new entity data.")
    status: str = Field(default="PENDING", description="'PENDING', 'APPROVED', 'REJECTED'")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIReviewQueueService:
    """
    Holds AI-generated suggestions until a human expert (MASTER_EDITOR)
    can review and apply them to the Enterprise Knowledge Graph.
    """
    def __init__(self):
        self._queue: Dict[str, AIReviewSuggestion] = {}
        logger.info("AI Review Queue Initialized.")

    def enqueue_suggestion(self, suggestion_type: str, confidence: float, payload: Dict[str, Any], target_entity_id: str = None) -> AIReviewSuggestion:
        """Pushes a new suggestion from the AI Orchestrator into the queue."""
        sug = AIReviewSuggestion(
            suggestion_type=suggestion_type,
            ai_confidence=confidence,
            payload=payload,
            target_entity_id=target_entity_id
        )
        self._queue[sug.id] = sug
        logger.info(f"Enqueued AI Suggestion: {sug.id} ({suggestion_type})")
        return sug

    def get_pending_suggestions(self) -> List[AIReviewSuggestion]:
        """Retrieves all suggestions waiting for human review."""
        return [s for s in self._queue.values() if s.status == "PENDING"]

    def review_suggestion(self, suggestion_id: str, approved: bool, editor_id: str) -> AIReviewSuggestion:
        """Processes the editor's decision."""
        if suggestion_id not in self._queue:
            raise NotFoundException(message=f"Suggestion {suggestion_id} not found.")
            
        sug = self._queue[suggestion_id]
        if sug.status != "PENDING":
            raise ValueError(f"Suggestion {suggestion_id} has already been processed.")
            
        sug.status = "APPROVED" if approved else "REJECTED"
        logger.info(f"Editor {editor_id} {sug.status} suggestion {suggestion_id}")
        
        # Note: If APPROVED, the frontend should take the `payload` and send it to the 
        # MetadataEngine or RelationshipEngine to actually apply the changes.
        return sug
