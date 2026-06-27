from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from .router import ai_router
from modules.conversations.models import ContextBlock

logger = logging.getLogger("CopilotAPI")
router = APIRouter(prefix="/ai", tags=["AI Copilot"])

class CopilotChatRequest(BaseModel):
    prompt: str
    user_id: str
    session_id: str
    context_block: ContextBlock

@router.post("/copilot/chat")
async def copilot_chat(request: CopilotChatRequest):
    """
    Endpoint for the frontend Copilot panel to send messages.
    """
    try:
        response = await ai_router.route_copilot_request(
            prompt=request.prompt,
            user_id=request.user_id,
            conv_id=request.session_id,
            context_block=request.context_block
        )
        return response
    except Exception as e:
        logger.error(f"Copilot chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
