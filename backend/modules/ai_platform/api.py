"""
API Router for Enterprise AI Orchestration Platform (EP-08).
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Form, Query, HTTPException

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import AIChatRequest, AIChatResponse, LLMGenerationOptions
from .orchestrator import AIOrchestrator
from .conversation import ConversationService
from .skills.skill_registry import SkillRegistry
from .recommendations import AIRecommendationEngine
from .observability import AIObservabilityService
from .providers.provider_registry import ProviderRegistry

logger = logging.getLogger("AIPlatform.API")
router = APIRouter(prefix="/api/v1/ai", tags=["Enterprise AI Platform"])


# ─────────────────────────────────────────────
# Chat
# ─────────────────────────────────────────────

@router.post("/chat", response_model=AIChatResponse)
async def chat(
    query: str = Form(...),
    skill: str = Form("knowledge_qa"),
    conversation_id: Optional[str] = Form(None),
    user_department: Optional[str] = Form(None),
    orchestrator: AIOrchestrator = Depends(lambda: container.resolve(AIOrchestrator)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """
    Primary enterprise AI chat endpoint.
    Routes through the full orchestration pipeline:
    Auth → Context Retrieval → Guard → Prompt → LLM → Validation → Citations → Response.
    """
    request = AIChatRequest(
        query=query,
        conversation_id=conversation_id,
        skill=skill,
        user_department=user_department or "GENERAL",
        user_roles=auth_context.get("roles", ["USER"]),
        options=LLMGenerationOptions()
    )
    try:
        return await orchestrator.chat(request)
    except Exception as e:
        logger.error(f"Chat orchestration failed: {e}")
        raise HTTPException(status_code=500, detail="AI service temporarily unavailable.")


# ─────────────────────────────────────────────
# Conversations
# ─────────────────────────────────────────────

@router.post("/conversations")
async def create_conversation(
    linked_entity_id: Optional[str] = Form(None),
    linked_workflow_id: Optional[str] = Form(None),
    conversation_svc: ConversationService = Depends(lambda: container.resolve(ConversationService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Creates a new persistent conversation session."""
    user_id = auth_context.get("sub", "system")
    conv = conversation_svc.create(user_id, linked_entity_id, linked_workflow_id)
    return {"conversation_id": conv.conversation_id, "user_id": conv.user_id}


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    conversation_svc: ConversationService = Depends(lambda: container.resolve(ConversationService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    conv = conversation_svc.get(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return conv


@router.get("/conversations")
async def list_my_conversations(
    conversation_svc: ConversationService = Depends(lambda: container.resolve(ConversationService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    user_id = auth_context.get("sub", "system")
    return conversation_svc.list_for_user(user_id)


# ─────────────────────────────────────────────
# Skills
# ─────────────────────────────────────────────

@router.get("/skills")
async def list_skills(
    skill_registry: SkillRegistry = Depends(lambda: container.resolve(SkillRegistry)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Lists all registered AI skills and their enabled status."""
    return skill_registry.list_skills()


@router.post("/skills/{skill_id}/disable")
async def disable_skill(
    skill_id: str,
    skill_registry: SkillRegistry = Depends(lambda: container.resolve(SkillRegistry)),
    auth_context: dict = Depends(require_authenticated_user)
):
    skill_registry.disable(skill_id)
    return {"message": f"Skill '{skill_id}' disabled."}


@router.post("/skills/{skill_id}/enable")
async def enable_skill(
    skill_id: str,
    skill_registry: SkillRegistry = Depends(lambda: container.resolve(SkillRegistry)),
    auth_context: dict = Depends(require_authenticated_user)
):
    skill_registry.enable(skill_id)
    return {"message": f"Skill '{skill_id}' enabled."}


# ─────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────

@router.get("/recommendations")
async def get_recommendations(
    query: str = Query(...),
    department: Optional[str] = Query(None),
    rec_engine: AIRecommendationEngine = Depends(lambda: container.resolve(AIRecommendationEngine)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Generates metadata-driven recommendations based on query intent. Requires user review."""
    recs = rec_engine.generate_for_context(
        query=query,
        user_department=department,
        context_asset_ids=[]
    )
    return [r.to_dict() for r in recs]


# ─────────────────────────────────────────────
# Administration
# ─────────────────────────────────────────────

@router.get("/admin/providers")
async def list_providers(
    provider_registry: ProviderRegistry = Depends(lambda: container.resolve(ProviderRegistry)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Lists all registered LLM providers."""
    return {"providers": provider_registry.list_providers()}


@router.get("/admin/observability")
async def get_observability_summary(
    obs: AIObservabilityService = Depends(lambda: container.resolve(AIObservabilityService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Returns AI usage analytics: latency, token counts, skill usage, validation failures."""
    return obs.get_summary()
