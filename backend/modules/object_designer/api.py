from fastapi import APIRouter, Depends
from typing import List
from core.di import container

from .service import ObjectDesignerService
from modules.object_definitions.templates import VisualObjectDefinition
from modules.content_management.api import require_master_editor

router = APIRouter(prefix="/api/v1/designer", tags=["Enterprise Object Designer"])

@router.get("/blueprints", response_model=List[VisualObjectDefinition])
async def list_blueprints(
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Lists all visual object blueprints (drafts and active)."""
    return designer.list_blueprints()

@router.post("/blueprints", response_model=VisualObjectDefinition)
async def save_blueprint(
    payload: VisualObjectDefinition,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Saves a visual object definition."""
    return designer.save_blueprint(payload)

@router.post("/blueprints/{blueprint_id}/publish")
async def publish_blueprint(
    blueprint_id: str,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Compiles the blueprint and pushes it to the live Entity Engine."""
    return designer.publish_blueprint(blueprint_id)
