"""
Governance Platform API (EP-09).
"""
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import (
    EnterprisePolicy, PolicyType, PolicyStatus, ClassificationLevel, ClassificationTag,
    GovernanceReviewPackage, GovernanceChangeType, ComplianceRecord
)
from .policy_engine import EnterprisePolicyEngine
from .field_security import FieldSecurityService
from .classification import ClassificationService
from .security_monitor import SecurityMonitor
from .compliance import ComplianceFramework
from .governance_engine import GovernanceEngine
from .audit_platform import EnterpriseAuditPlatform

logger = logging.getLogger("Governance.API")
router = APIRouter(prefix="/api/v1/governance", tags=["Enterprise Governance Platform"])


# ── Policy Management ──────────────────────────────────────────

@router.get("/policies", response_model=List[EnterprisePolicy])
async def list_policies(
    policy_type: Optional[PolicyType] = None,
    engine: EnterprisePolicyEngine = Depends(lambda: container.resolve(EnterprisePolicyEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    if policy_type:
        return engine.get_policies_by_type(policy_type)
    # Exposing internal structure for admin view
    return list(engine._policies.values())


# ── Classification ─────────────────────────────────────────────

@router.get("/classifications")
async def list_classification_tags(
    classification_svc: ClassificationService = Depends(lambda: container.resolve(ClassificationService)),
    auth: dict = Depends(require_authenticated_user)
):
    return classification_svc.get_all_tags()


@router.post("/classifications")
async def tag_asset(
    payload: Dict[str, Any] = Body(...),
    classification_svc: ClassificationService = Depends(lambda: container.resolve(ClassificationService)),
    auth: dict = Depends(require_authenticated_user)
):
    asset_id = payload.get("asset_id")
    asset_type = payload.get("asset_type")
    level = payload.get("level")
    
    if not all([asset_id, asset_type, level]):
        raise HTTPException(status_code=400, detail="Missing required fields: asset_id, asset_type, level")
        
    try:
        level_enum = ClassificationLevel(level)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid classification level: {level}")
        
    return classification_svc.tag_asset(str(asset_id), str(asset_type), level_enum, actor_id=auth.get("sub", "system"))


# ── Field Security ─────────────────────────────────────────────

@router.get("/field-security/{object_type}")
async def get_field_security(
    object_type: str,
    field_svc: FieldSecurityService = Depends(lambda: container.resolve(FieldSecurityService)),
    auth: dict = Depends(require_authenticated_user)
):
    """Admin view of all registered field policies for an object type."""
    return [p for p in field_svc._field_policies if p.object_type == object_type]


# ── Governance Reviews ─────────────────────────────────────────

@router.get("/reviews")
async def list_pending_reviews(
    gov_engine: GovernanceEngine = Depends(lambda: container.resolve(GovernanceEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return gov_engine.get_pending_reviews()


@router.post("/reviews/{package_id}/approve")
async def approve_review(
    package_id: str,
    gov_engine: GovernanceEngine = Depends(lambda: container.resolve(GovernanceEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []) and "SECURITY_OFFICER" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Requires ADMIN or SECURITY_OFFICER role.")
    try:
        return gov_engine.approve_change(package_id, auth.get("sub", "system"))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{package_id}/reject")
async def reject_review(
    package_id: str,
    payload: Dict[str, str] = Body(...),
    gov_engine: GovernanceEngine = Depends(lambda: container.resolve(GovernanceEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []) and "SECURITY_OFFICER" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Requires ADMIN or SECURITY_OFFICER role.")
    try:
        reason = payload.get("reason", "No reason provided")
        return gov_engine.reject_change(package_id, auth.get("sub", "system"), reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Security Analytics ─────────────────────────────────────────

@router.get("/security/analytics")
async def get_security_analytics(
    monitor: SecurityMonitor = Depends(lambda: container.resolve(SecurityMonitor)),
    auth: dict = Depends(require_authenticated_user)
):
    return monitor.get_analytics()


@router.get("/security/events")
async def get_security_events(
    limit: int = Query(100),
    monitor: SecurityMonitor = Depends(lambda: container.resolve(SecurityMonitor)),
    auth: dict = Depends(require_authenticated_user)
):
    return monitor.get_events(limit)


# ── Compliance ─────────────────────────────────────────────────

@router.get("/compliance")
async def get_compliance_records(
    standard: Optional[str] = Query(None),
    comp_framework: ComplianceFramework = Depends(lambda: container.resolve(ComplianceFramework)),
    auth: dict = Depends(require_authenticated_user)
):
    return comp_framework.get_records(standard)
