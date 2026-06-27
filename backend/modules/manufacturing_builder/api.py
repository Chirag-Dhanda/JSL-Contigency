from fastapi import APIRouter, Depends
from typing import List
from core.di import container

from .service import ManufacturingBuilderService
from modules.process_modeling.models import ManufacturingFlow
from modules.content_management.api import require_master_editor

router = APIRouter(prefix="/api/v1/flow-builder", tags=["Enterprise Manufacturing Flow Builder"])

@router.get("/flows", response_model=List[ManufacturingFlow])
async def list_flows(
    builder: ManufacturingBuilderService = Depends(lambda: container.resolve(ManufacturingBuilderService)),
    auth_context: dict = Depends(require_master_editor)
):
    return builder.list_flows()

@router.post("/flows", response_model=ManufacturingFlow)
async def save_flow(
    payload: ManufacturingFlow,
    builder: ManufacturingBuilderService = Depends(lambda: container.resolve(ManufacturingBuilderService)),
    auth_context: dict = Depends(require_master_editor)
):
    return builder.save_flow(payload)

@router.post("/flows/{flow_id}/publish")
async def publish_flow(
    flow_id: str,
    builder: ManufacturingBuilderService = Depends(lambda: container.resolve(ManufacturingBuilderService)),
    auth_context: dict = Depends(require_master_editor)
):
    return builder.publish_flow(flow_id, auth_context.get("sub", "system"))

@router.get("/flows/{flow_id}/ai-suggestions")
async def get_flow_suggestions(
    flow_id: str,
    builder: ManufacturingBuilderService = Depends(lambda: container.resolve(ManufacturingBuilderService)),
    auth_context: dict = Depends(require_master_editor)
):
    return builder.get_ai_suggestions(flow_id)
