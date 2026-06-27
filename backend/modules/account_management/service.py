from exceptions.base import SystemException
from typing import Optional
from .models import OnboardingRequest, ApprovalWorkflow
from logging import getLogger

logger = getLogger("AccountManagementService")

class AccountProvisioningService:
    """Coordinates the complex lifecycle of creating a user."""
    
    async def provision_user(self, payload: dict, requested_by: str) -> str:
        """
        Orchestrates:
        1. Checking Policies (via PolicyEngine).
        2. Creating UserEntity.
        3. Firing OnboardingRequest (Email trigger placeholder).
        """
        raise SystemException("Not Implemented: provision_user workflow")

    async def generate_invitation(self, user_id: str) -> OnboardingRequest:
        raise SystemException("Not Implemented: generate_invitation")

class ApprovalWorkflowService:
    """Manages the state transitions for HR approvals."""
    
    async def get_pending_approvals(self, approver_id: str) -> list[ApprovalWorkflow]:
        raise SystemException("Not Implemented: get_pending_approvals")
        
    async def process_approval_step(self, workflow_id: str, approver_id: str, step: str) -> bool:
        raise SystemException("Not Implemented: process_approval_step")
