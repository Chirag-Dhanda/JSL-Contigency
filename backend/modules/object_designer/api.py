from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from core.di import container

from .service import ObjectDesignerService
from .models import BlueprintDraft, ReviewPackage
from modules.content_management.api import require_master_editor

router = APIRouter(prefix="/api/v1/designer", tags=["Enterprise Object Designer"])

@router.post("/blueprints", response_model=BlueprintDraft)
async def create_blueprint(
    payload: BlueprintDraft,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Creates a new metadata Blueprint Draft."""
    return designer.create_blueprint(payload)

@router.put("/blueprints/{blueprint_id}", response_model=BlueprintDraft)
async def update_blueprint(
    blueprint_id: str,
    payload: BlueprintDraft,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Updates an existing Blueprint Draft."""
    return designer.update_blueprint(blueprint_id, payload)

@router.post("/blueprints/{blueprint_id}/duplicate", response_model=BlueprintDraft)
async def duplicate_blueprint(
    blueprint_id: str,
    new_type_id: str,
    new_display_name: str,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Duplicates an existing blueprint."""
    return designer.duplicate_blueprint(blueprint_id, new_type_id, new_display_name)

@router.get("/blueprints/{blueprint_id}/review-package", response_model=ReviewPackage)
async def get_review_package(
    blueprint_id: str,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Generates a comprehensive review package for approval."""
    return designer.generate_review_package(blueprint_id)

@router.post("/blueprints/{blueprint_id}/publish")
async def publish_blueprint(
    blueprint_id: str,
    designer: ObjectDesignerService = Depends(lambda: container.resolve(ObjectDesignerService)),
    auth_context: dict = Depends(require_master_editor)
):
    """Validates and publishes the blueprint to the active Enterprise Registry."""
    return designer.publish_blueprint(blueprint_id, auth_context.get("sub", "system"))
