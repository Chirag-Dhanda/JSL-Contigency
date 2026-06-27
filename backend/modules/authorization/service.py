from exceptions.base import SystemException, AuthorizationException
from .models import ResourceOwnership
from modules.permissions.service import PermissionEngine
from logging import getLogger

logger = getLogger("AuthorizationPipeline")

class AuthorizationPipeline:
    """The central enterprise authorization engine."""
    
    def __init__(self, permission_engine: PermissionEngine):
        self._permissions = permission_engine

    async def evaluate_access(
        self, 
        actor_id: str, 
        actor_dept_id: str,
        required_permission: str, 
        resource_ownership: ResourceOwnership
    ) -> dict:
        """
        The central enterprise authorization flow:
        Returns a dict: {"granted": bool, "overview_only": bool}
        """
        logger.debug(f"Evaluating access for {actor_id} requiring {required_permission}")
        
        # 1. RBAC Check (Does the user's role even allow this action?)
        has_perm = await self._permissions.has_explicit_permission(actor_id, required_permission)
        if not has_perm:
            return {"granted": False, "overview_only": False}
            
        # 2. Same Department Check (Fast path)
        if actor_dept_id == resource_ownership.owned_by_dept_id:
            return {"granted": True, "overview_only": False}
            
        # 3. Cross-Department Temporary Access Check
        # Lazy load to prevent circular initialization
        from core.di import container
        from modules.access_request.service import AccessRequestService
        access_svc = container.resolve(AccessRequestService)
        
        temp_grants = await access_svc.get_active_temporary_grants(actor_id)
        for grant in temp_grants:
            # Check if grant covers this specific resource and permission
            if grant.target_resource == resource_ownership.resource_id and grant.requested_permission == required_permission:
                logger.info(f"Access granted via temporary exception {grant.id} for user {actor_id}")
                return {"granted": True, "overview_only": False}
                
        # 4. Overview Access Fallback
        # If RBAC allows it, but it's cross-department and no temporary grant exists, yield Overview Access.
        logger.warning(f"Cross-department strict access denied for {actor_id}. Yielding Overview Access.")
        return {"granted": False, "overview_only": True}

    async def require_access(
        self, 
        actor_id: str, 
        actor_dept_id: str,
        required_permission: str, 
        resource_ownership: ResourceOwnership
    ) -> bool:
        """
        Evaluates access and throws AuthorizationException if denied completely.
        Returns True if full access is granted, False if only Overview Access is granted.
        """
        result = await self.evaluate_access(actor_id, actor_dept_id, required_permission, resource_ownership)
        if result["granted"]:
            return True
        elif result["overview_only"]:
            return False
        else:
            raise AuthorizationException(message="Access Denied by Enterprise Authorization Engine.")
