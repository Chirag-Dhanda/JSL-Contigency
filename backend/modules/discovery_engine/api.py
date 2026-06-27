from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
from core.di import container

from .service import DiscoveryEngineService
from modules.hyperlink_engine.service import HyperlinkEngineService

router = APIRouter(prefix="/api/discovery", tags=["Discovery Engine"])

class HyperlinkRequest(BaseModel):
    text: str

@router.get("/{entity_id}", response_model=Dict[str, Any])
async def get_discovery_profile(entity_id: str):
    discovery_service: DiscoveryEngineService = container.resolve("DiscoveryEngineService")
    try:
        return discovery_service.get_discovery_profile(entity_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
        
@router.post("/hyperlink", response_model=Dict[str, str])
async def inject_hyperlinks(req: HyperlinkRequest):
    """
    Utility endpoint to test hyperlink injection.
    """
    hyperlink_service: HyperlinkEngineService = container.resolve("HyperlinkEngineService")
    linked_text = hyperlink_service.inject_hyperlinks(req.text)
    return {"linked_text": linked_text}
