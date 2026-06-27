from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .enums import RequestStatus, DurationType

class AccessRequestEntity(BaseModel):
    """Tracks a user's request for elevated or cross-department access."""
    id: str
    requester_id: str
    target_resource: str
    requested_permission: str
    business_justification: str
    priority: int = 1
    
    duration_type: DurationType
    requested_duration_minutes: Optional[int] = None
    
    status: RequestStatus = RequestStatus.PENDING
    
    submitted_at: datetime
    approved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    approver_id: Optional[str] = None
