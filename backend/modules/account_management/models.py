from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from modules.users.enums import EmployeeStatus

class OnboardingRequest(BaseModel):
    """Tracks the process of a new employee joining the system."""
    id: str
    user_id: str
    invitation_token: str
    temporary_password_hash: Optional[str] = None
    expires_at: datetime
    is_activated: bool = False
    
    # Future multi-channel integration
    invite_email_sent: bool = False

class ApprovalWorkflow(BaseModel):
    """State machine tracking the progression of an account's approval."""
    id: str
    target_user_id: str
    requested_by_id: str
    
    # Workflow Progression
    is_manager_approved: bool = False
    manager_id: Optional[str] = None
    
    is_dept_head_approved: bool = False
    dept_head_id: Optional[str] = None
    
    is_hr_approved: bool = False
    hr_approver_id: Optional[str] = None
    
    final_status: EmployeeStatus = EmployeeStatus.PENDING_APPROVAL

class AuditLog(BaseModel):
    """Immutable ledger of all critical user lifecycle actions."""
    id: str
    action: str  # e.g., 'USER_CREATED', 'ROLE_CHANGED'
    actor_id: str
    target_id: str
    timestamp: datetime
    metadata_snapshot: dict
