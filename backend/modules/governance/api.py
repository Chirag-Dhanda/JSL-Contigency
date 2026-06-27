from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from core.di import container

from .models import AuditRecord, VersionRecord, LifecycleState
from modules.publishing_engine.service import PublishingEngineService
from modules.version_engine.service import VersionEngineService
from modules.audit_engine.service import AuditEngineService
from modules.compliance.service import ComplianceEngineService

router = APIRouter(prefix="/api/governance", tags=["Governance Platform"])

@router.get("/entity/{entity_id}/state")
async def get_state(entity_id: str):
    pub: PublishingEngineService = container.resolve("PublishingEngineService")
    return {"state": pub.get_state(entity_id)}

@router.get("/entity/{entity_id}/versions", response_model=List[VersionRecord])
async def get_versions(entity_id: str):
    ver: VersionEngineService = container.resolve("VersionEngineService")
    return ver.get_version_history(entity_id)

@router.get("/entity/{entity_id}/audit", response_model=List[AuditRecord])
async def get_audit(entity_id: str):
    aud: AuditEngineService = container.resolve("AuditEngineService")
    return aud.get_history_for_entity(entity_id)

@router.post("/entity/{entity_id}/publish")
async def publish_entity(entity_id: str, user_id: str = "u-demo", notes: str = ""):
    pub: PublishingEngineService = container.resolve("PublishingEngineService")
    try:
        pub.publish(entity_id, user_id, notes)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
