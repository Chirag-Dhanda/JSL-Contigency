from exceptions.base import SystemException
from typing import Optional, Dict
from datetime import datetime, timezone, timedelta
from .models import AccessRequestEntity
from .enums import RequestStatus, DurationType
from core.di import container
from modules.audit.service import AuditService
from modules.notifications.hooks import NotificationHooks
from logging import getLogger
import uuid

logger = getLogger("AccessRequestService")

class AccessRequestService:
    """Manages the creation and approval workflow for Access Requests."""
    
    def __init__(self):
        self._requests: Dict[str, AccessRequestEntity] = {}
        
    async def create_request(self, requester_id: str, target_resource: str, perm: str, justification: str, duration: DurationType) -> str:
        req_id = str(uuid.uuid4())
        req = AccessRequestEntity(
            id=req_id,
            requester_id=requester_id,
            target_resource=target_resource,
            requested_permission=perm,
            business_justification=justification,
            duration_type=duration,
            submitted_at=datetime.now(timezone.utc)
        )
        self._requests[req_id] = req
        
        # Log & Notify
        audit = container.resolve(AuditService)
        await audit.log_event("ACCESS_REQUEST_CREATED", requester_id, target_resource_id=req_id)
        await NotificationHooks.on_access_request_created(req_id, requester_id)
        
        return req_id
        
    async def approve_request(self, req_id: str, approver_id: str, active_minutes: int = 60) -> None:
        req = self._requests.get(req_id)
        if not req:
            raise SystemException("Request not found")
            
        req.status = RequestStatus.APPROVED
        req.approver_id = approver_id
        req.approved_at = datetime.now(timezone.utc)
        
        if req.duration_type != DurationType.PERMANENT:
            req.expires_at = req.approved_at + timedelta(minutes=active_minutes)
            
        # Log & Notify
        audit = container.resolve(AuditService)
        await audit.log_event("ACCESS_REQUEST_APPROVED", approver_id, target_resource_id=req_id)
        await NotificationHooks.on_access_request_approved(req_id, approver_id)

    async def get_active_temporary_grants(self, requester_id: str) -> list[AccessRequestEntity]:
        """Used by the AuthorizationEngine to check if a user has an approved, unexpired request."""
        active = []
        now = datetime.now(timezone.utc)
        for req in self._requests.values():
            if req.requester_id == requester_id and req.status == RequestStatus.APPROVED:
                if req.expires_at and req.expires_at < now:
                    req.status = RequestStatus.EXPIRED # Auto-expire lazy evaluation
                    logger.info(f"Temporary Access {req.id} automatically expired.")
                else:
                    active.append(req)
        return active
