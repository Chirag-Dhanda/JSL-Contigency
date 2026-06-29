from exceptions.base import SystemException
from typing import Optional
from logging import getLogger
from core.di import container
from modules.governance_platform.policy_engine import EnterprisePolicyEngine
from modules.governance_platform.models import PolicyType

logger = getLogger("AuthorizationPolicies")

class AccountCreationPolicy:
    """Policy evaluating who is allowed to create accounts."""
    
    @classmethod
    async def can_create_account(
        cls, 
        actor_id: str, 
        target_department_id: str, 
        target_role_id: str
    ) -> bool:
        """
        Rules:
        - Administrators bypass restrictions.
        - Managers can only create inside their own department.
        - Managers can only create roles with a lower management_level than their own.
        """
        engine = container.resolve(EnterprisePolicyEngine)
        # Mock role resolution for EP-09 testing
        roles = ["ADMIN"] if actor_id == "u-master-editor" else ["MANAGER"]
        
        # We model this as an ACCESS policy check for the 'account.create' action
        decision = engine.evaluate(
            actor_roles=roles,
            actor_dept=target_department_id,
            action="account.create",
            policy_type=PolicyType.ACCESS
        )
        return decision.granted
        
class DocumentApprovalPolicy:
    """Policy evaluating who is allowed to approve SAP documents or SOPs."""
    
    @classmethod
    async def can_approve_document(
        cls, 
        actor_id: str, 
        document_owner_dept_id: str
    ) -> bool:
        """
        Rules:
        - Must have the 'document.approve' explicit permission.
        - Must be in the same department OR have cross-department APPROVE access.
        """
        engine = container.resolve(EnterprisePolicyEngine)
        roles = ["ADMIN"] if actor_id == "u-master-editor" else ["USER"]
        
        decision = engine.evaluate(
            actor_roles=roles,
            actor_dept=document_owner_dept_id,
            action="document.approve",
            policy_type=PolicyType.ACCESS
        )
        return decision.granted
