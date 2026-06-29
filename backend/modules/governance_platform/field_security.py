"""
Field-Level Security Service (EP-09).
Resolves field visibility metadata for a given user context.
"""
import logging
from typing import List, Dict, Optional, Any

from .models import FieldPermission, FieldVisibility, ClassificationLevel, CLASSIFICATION_RANK

logger = logging.getLogger("Governance.FieldSecurity")


class FieldSecurityService:
    """
    Determines visibility of specific object fields based on metadata policies.
    """

    def __init__(self):
        self._field_policies: List[FieldPermission] = []

    def register_policy(self, policy: FieldPermission) -> None:
        self._field_policies.append(policy)
        logger.debug(f"Registered field policy: {policy.object_type}.{policy.field_name} -> {policy.visibility}")

    def get_field_visibility(
        self,
        object_type: str,
        field_name: str,
        user_roles: List[str],
        user_dept: Optional[str] = None
    ) -> FieldVisibility:
        """
        Determines the visibility of a field for the given user.
        Defaults to VISIBLE if no policy exists.
        """
        user_roles_upper = {r.upper() for r in user_roles}
        
        # Admin bypass
        if "ADMIN" in user_roles_upper or "SYSTEM" in user_roles_upper:
            return FieldVisibility.VISIBLE

        # Find applicable policy
        policy = next((p for p in self._field_policies if p.object_type == object_type and p.field_name == field_name), None)
        if not policy:
            return FieldVisibility.VISIBLE  # Default open if unconfigured

        # 1. Classification check
        user_clearance = self._resolve_clearance(user_roles_upper)
        field_rank = CLASSIFICATION_RANK.get(policy.classification, 0)
        if user_clearance < field_rank:
            return FieldVisibility.HIDDEN

        # 2. Role check
        if policy.required_roles:
            policy_roles_upper = {r.upper() for r in policy.required_roles}
            if not (user_roles_upper & policy_roles_upper):
                return FieldVisibility.HIDDEN

        # 3. Dept check
        if policy.required_depts and user_dept:
            if user_dept not in policy.required_depts:
                return FieldVisibility.HIDDEN

        # If it passes all restrictions, apply the defined visibility (which might be READ_ONLY or MASKED)
        # However, for EP-09, if it's restricted by dept and they match, it's visible. 
        # If the policy dictates MASKED or READ_ONLY for *everyone* allowed to see it:
        return policy.visibility

    def filter_payload(
        self,
        object_type: str,
        proposed_state: Dict[str, Any],
        current_state: Optional[Dict[str, Any]] = None,
        impact_analysis: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Filters a dictionary payload, removing or masking fields the user cannot see.
        """
        filtered = {}
        for field, value in proposed_state.items():
            visibility = self.get_field_visibility(object_type, field, [], None)
            
            if visibility == FieldVisibility.VISIBLE:
                filtered[field] = value
            elif visibility == FieldVisibility.READ_ONLY:
                filtered[field] = value  # Same as visible for read payloads
            elif visibility == FieldVisibility.MASKED:
                filtered[field] = self._mask_value(value)
            elif visibility == FieldVisibility.HIDDEN or visibility == FieldVisibility.DEPT_RESTRICTED:
                continue  # Omit field
                
        return filtered

    def _mask_value(self, value: Any) -> Any:
        """Applies basic data masking."""
        if value is None:
            return None
        s_val = str(value)
        if len(s_val) <= 4:
            return "****"
        return "*" * (len(s_val) - 4) + s_val[-4:]

    def _resolve_clearance(self, roles: set) -> int:
        ROLE_CLEARANCE = {
            "ADMIN": 6, "SECURITY_OFFICER": 6, "KNOWLEDGE_MANAGER": 4,
            "MANAGER": 3, "SUPERVISOR": 2, "USER": 1, "VIEWER": 0,
        }
        return max((ROLE_CLEARANCE.get(r, 1) for r in roles), default=1)
