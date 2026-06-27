from exceptions.base import SystemException
from typing import Optional
from logging import getLogger

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
        raise SystemException("Not Implemented: can_create_account policy")
        
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
        raise SystemException("Not Implemented: can_approve_document policy")
