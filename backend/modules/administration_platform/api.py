"""
Administration Platform API (EP-13).
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Body

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import (
    ConfigurationSetting, ConfigurationVersion, FeatureFlag, 
    ReviewQueueItem, TenantEnvironment
)
from .config_manager import ConfigManager
from .feature_flags import FeatureManager
from .review_center import ReviewCenter
from .versioning import VersionManager
from .environment import EnvironmentManager

router = APIRouter(prefix="/api/v1/admin", tags=["Enterprise Administration"])

# ── Dependency Helpers ───────────────────────────────────────────────────────

def require_admin(auth: dict = Depends(require_authenticated_user)) -> dict:
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Administrator privileges required.")
    return auth

# ── Configuration Platform ───────────────────────────────────────────────────

@router.get("/config", response_model=List[ConfigurationSetting])
async def get_all_config(
    config_mgr: ConfigManager = Depends(lambda: container.resolve(ConfigManager)),
    auth: dict = Depends(require_admin)
):
    return config_mgr.get_all_settings()

@router.put("/config/{key}", response_model=ConfigurationSetting)
async def update_config(
    key: str,
    payload: Dict[str, Any] = Body(...),
    config_mgr: ConfigManager = Depends(lambda: container.resolve(ConfigManager)),
    auth: dict = Depends(require_admin)
):
    if "value" not in payload:
        raise HTTPException(status_code=400, detail="Missing 'value' in payload")
    
    return config_mgr.set_setting(
        key=key, 
        value=payload["value"], 
        updated_by=auth.get("sub", "admin"),
        description=payload.get("description", "")
    )

@router.get("/versions", response_model=List[ConfigurationVersion])
async def get_versions(
    version_mgr: VersionManager = Depends(lambda: container.resolve(VersionManager)),
    auth: dict = Depends(require_admin)
):
    return version_mgr.get_history()

# ── Feature Management ───────────────────────────────────────────────────────

@router.get("/features", response_model=List[FeatureFlag])
async def get_features(
    feature_mgr: FeatureManager = Depends(lambda: container.resolve(FeatureManager)),
    auth: dict = Depends(require_admin)
):
    return feature_mgr.get_all_flags()

@router.post("/features")
async def register_feature(
    flag: FeatureFlag,
    feature_mgr: FeatureManager = Depends(lambda: container.resolve(FeatureManager)),
    auth: dict = Depends(require_admin)
):
    feature_mgr.set_flag(flag, updated_by=auth.get("sub", "admin"))
    return flag

# ── Review & Approval Center ─────────────────────────────────────────────────

@router.get("/review-queue", response_model=List[ReviewQueueItem])
async def get_review_queue(
    status: Optional[str] = None,
    review_center: ReviewCenter = Depends(lambda: container.resolve(ReviewCenter)),
    auth: dict = Depends(require_admin)
):
    # Convert string status to enum safely
    from .models import ReviewStatus
    enum_status = None
    if status:
        try:
            enum_status = ReviewStatus(status.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status filter")
            
    return review_center.get_queue(status=enum_status)

@router.post("/review-queue/{queue_id}/process", response_model=ReviewQueueItem)
async def process_review_item(
    queue_id: str,
    payload: Dict[str, str] = Body(...),
    review_center: ReviewCenter = Depends(lambda: container.resolve(ReviewCenter)),
    auth: dict = Depends(require_admin)
):
    action = payload.get("action")
    notes = payload.get("notes", "")
    if action not in ["APPROVE", "REJECT"]:
        raise HTTPException(status_code=400, detail="Action must be APPROVE or REJECT")
        
    try:
        return review_center.process_review(
            queue_id=queue_id, 
            action=action, 
            reviewer=auth.get("sub", "admin"), 
            notes=notes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ── Environment Management ───────────────────────────────────────────────────

@router.get("/environments", response_model=List[TenantEnvironment])
async def get_environments(
    env_mgr: EnvironmentManager = Depends(lambda: container.resolve(EnvironmentManager)),
    auth: dict = Depends(require_admin)
):
    return env_mgr.get_all_environments()
