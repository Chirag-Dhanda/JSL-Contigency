from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from core.di import container

from .ai_review import AIReviewQueueService
from modules.metadata_engine.service import MetadataEngineService
from modules.content_management.api import require_master_editor

router = APIRouter(prefix="/api/v1/studio", tags=["Enterprise Knowledge Studio"])

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    auth_context: dict = Depends(require_master_editor),
    meta_engine: MetadataEngineService = Depends(lambda: container.resolve(MetadataEngineService)),
    review_queue: AIReviewQueueService = Depends(lambda: container.resolve(AIReviewQueueService))
):
    """
    Aggregates data for the Knowledge Studio landing page.
    Requires MASTER_EDITOR permissions.
    """
    # 1. Count Total Entities (Mock logic for dict)
    total_entities = len(meta_engine._entities)
    
    # 2. Find Drafts needing review
    # We would normally use a DB query `WHERE status = 'DRAFT'`
    drafts = [e for e in meta_engine._entities.values() if e.status.value == "DRAFT"]
    
    # 3. Get pending AI reviews
    pending_ai_suggestions = review_queue.get_pending_suggestions()
    
    # 4. Generate Activity Feed (Mocked for Stage 5.3)
    activity_feed = [
        {"action": "PUBLISHED", "entity": "SOP-EAF-01", "user": "system_admin", "time": "10 minutes ago"},
        {"action": "MEDIA_UPLOADED", "entity": "furnace_schematic.pdf", "user": auth_context.get("sub"), "time": "1 hour ago"}
    ]
    
    return {
        "metrics": {
            "total_entities": total_entities,
            "drafts_pending": len(drafts),
            "ai_reviews_pending": len(pending_ai_suggestions)
        },
        "recent_drafts": [{"id": d.id, "name": d.display_name, "type": d.entity_type} for d in drafts[:5]],
        "ai_queue_preview": [{"id": s.id, "type": s.suggestion_type, "confidence": s.ai_confidence} for s in pending_ai_suggestions[:5]],
        "activity_feed": activity_feed
    }

@router.post("/ai-queue/{suggestion_id}/review")
async def review_ai_suggestion(
    suggestion_id: str,
    approved: bool,
    review_queue: AIReviewQueueService = Depends(lambda: container.resolve(AIReviewQueueService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Accepts or rejects an AI suggestion."""
    return review_queue.review_suggestion(suggestion_id, approved, auth_context.get("sub"))
