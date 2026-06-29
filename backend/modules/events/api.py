"""
Event Platform API (EP-11).
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Body

from core.di import container
from modules.auth.middleware import require_authenticated_user

from .models import DomainEvent, EventSchema, AutomationRule, DLQRecord
from .bus import AdvancedEventBus
from .registry import EventRegistry
from .store import IEventStore
from .dlq import IDLQStorage
from .automation_engine import AutomationEngine

router = APIRouter(prefix="/api/v1/events", tags=["Enterprise Event Bus"])


@router.get("/catalog")
async def get_event_catalog(
    registry: EventRegistry = Depends(lambda: container.resolve(EventRegistry)),
    auth: dict = Depends(require_authenticated_user)
):
    return registry.get_catalog()

@router.post("/publish")
async def publish_event(
    event: DomainEvent,
    bus: AdvancedEventBus = Depends(lambda: container.resolve(AdvancedEventBus)),
    auth: dict = Depends(require_authenticated_user)
):
    # Set correlation if missing
    if not event.correlation_id:
        event.correlation_id = event.event_id
        
    await bus.publish(event)
    return {"message": "Event accepted"}

@router.get("/dlq")
async def get_dlq(
    dlq: IDLQStorage = Depends(lambda: container.resolve(IDLQStorage)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin privileges required.")
    return dlq.get_all_unresolved()

@router.post("/dlq/{dlq_id}/retry")
async def retry_dlq_event(
    dlq_id: str,
    dlq: IDLQStorage = Depends(lambda: container.resolve(IDLQStorage)),
    bus: AdvancedEventBus = Depends(lambda: container.resolve(AdvancedEventBus)),
    auth: dict = Depends(require_authenticated_user)
):
    if "ADMIN" not in auth.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin privileges required.")
        
    record = dlq.get_by_id(dlq_id)
    if not record:
        raise HTTPException(status_code=404, detail="DLQ record not found.")
        
    # Re-publish
    await bus.publish(record.event)
    
    # Mark resolved (in a real system, we'd wait for success, but simplified here)
    if hasattr(dlq, 'update_status'):
        dlq.update_status(dlq_id, "RESOLVED")
        
    return {"message": f"Event {record.event.event_id} requeued."}

@router.get("/automation-rules")
async def get_automation_rules(
    automation: AutomationEngine = Depends(lambda: container.resolve(AutomationEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    return list(automation._rules.values())

@router.post("/automation-rules")
async def register_automation_rule(
    rule: AutomationRule,
    automation: AutomationEngine = Depends(lambda: container.resolve(AutomationEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    # New rules must be created as DRAFT (is_active=False) if they require approval
    if rule.requires_approval:
        rule.is_active = False
    automation.register_rule(rule)
    return rule

@router.post("/automation-rules/{rule_id}/activate")
async def activate_automation_rule(
    rule_id: str,
    automation: AutomationEngine = Depends(lambda: container.resolve(AutomationEngine)),
    auth: dict = Depends(require_authenticated_user)
):
    try:
        pkg_id = automation.propose_activation(rule_id, auth.get("sub", "system"))
        return {"message": "Activation proposed.", "package_id": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
