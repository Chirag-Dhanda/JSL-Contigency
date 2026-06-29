"""
Integration Platform API (EP-10).
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import (
    ConnectorDefinition, SyncMode, MappingRule, ConflictRecord, SyncSchedule
)
from .gateway import IntegrationGateway
from .transformation import TransformationEngine
from .sync_engine import IntegrationSyncEngine
from .scheduler import IntegrationScheduler
from .conflict_engine import ConflictResolutionEngine
from .review import IntegrationReviewService

router = APIRouter(prefix="/api/v1/integration", tags=["Enterprise Integration Platform"])


# ── Connectors ───────────────────────────────────────────────────

@router.get("/connectors")
async def list_connectors(
    gateway: IntegrationGateway = Depends(lambda: container.resolve(IntegrationGateway)),
    auth: dict = Depends(require_authenticated_user)
):
    return list(gateway._definitions.values())

@router.post("/connectors")
async def register_connector(
    definition: ConnectorDefinition,
    gateway: IntegrationGateway = Depends(lambda: container.resolve(IntegrationGateway)),
    auth: dict = Depends(require_authenticated_user)
):
    gateway.register_definition(definition)
    return definition

@router.get("/connectors/{connector_id}/schema")
async def discover_schema(
    connector_id: str,
    gateway: IntegrationGateway = Depends(lambda: container.resolve(IntegrationGateway)),
    auth: dict = Depends(require_authenticated_user)
):
    try:
        return await gateway.discover_schema(connector_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/connectors/{connector_id}/activate")
async def request_activation(
    connector_id: str,
    review_svc: IntegrationReviewService = Depends(lambda: container.resolve(IntegrationReviewService)),
    auth: dict = Depends(require_authenticated_user)
):
    try:
        package_id = review_svc.propose_connector_activation(connector_id, auth.get("sub", "system"))
        return {"message": "Activation proposed for review.", "package_id": package_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Mappings & Transformations ───────────────────────────────────

@router.get("/mappings/{connector_id}")
async def get_mappings(
    connector_id: str,
    transformer: TransformationEngine = Depends(lambda: container.resolve(TransformationEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return transformer.get_mappings_for_connector(connector_id)

@router.post("/mappings")
async def register_mapping(
    mapping: MappingRule,
    transformer: TransformationEngine = Depends(lambda: container.resolve(TransformationEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    transformer.register_mapping(mapping)
    return mapping


# ── Synchronization & Scheduling ─────────────────────────────────

@router.post("/sync/{connector_id}")
async def trigger_sync(
    connector_id: str,
    entity_type: str = Query(..., description="E.g., Equipment"),
    mode: SyncMode = Query(SyncMode.DELTA),
    sync_engine: IntegrationSyncEngine = Depends(lambda: container.resolve(IntegrationSyncEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    try:
        results = await sync_engine.execute_sync(connector_id, mode, entity_type)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedules")
async def add_schedule(
    schedule: SyncSchedule,
    scheduler: IntegrationScheduler = Depends(lambda: container.resolve(IntegrationScheduler)),
    auth: dict = Depends(require_authenticated_user)
):
    scheduler.add_schedule(schedule)
    return schedule

@router.get("/schedules/{connector_id}")
async def get_schedules(
    connector_id: str,
    scheduler: IntegrationScheduler = Depends(lambda: container.resolve(IntegrationScheduler)),
    auth: dict = Depends(require_authenticated_user)
):
    return scheduler.get_schedules(connector_id)


# ── Conflicts ────────────────────────────────────────────────────

@router.get("/conflicts")
async def list_conflicts(
    connector_id: Optional[str] = Query(None),
    conflict_engine: ConflictResolutionEngine = Depends(lambda: container.resolve(ConflictResolutionEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return conflict_engine.get_unresolved_conflicts(connector_id)

@router.post("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(
    conflict_id: str,
    payload: Dict[str, str] = Body(...),
    conflict_engine: ConflictResolutionEngine = Depends(lambda: container.resolve(ConflictResolutionEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    action = payload.get("action", "IGNORE")
    try:
        conflict_engine.resolve_conflict(conflict_id, action)
        return {"message": "Conflict marked as resolved."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
