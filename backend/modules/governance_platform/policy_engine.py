"""
Enterprise Policy Engine (EP-09).
Evaluates metadata-driven policies for any enterprise operation.
No hardcoded permission checks. Policies are versioned data.
"""
import logging
from typing import List, Optional, Dict, Any

from .models import (
    EnterprisePolicy, PolicyDecision, PolicyType, PolicyStatus,
    ClassificationLevel, CLASSIFICATION_RANK, RLSContext
)

logger = logging.getLogger("Governance.PolicyEngine")


class EnterprisePolicyEngine:
    """
    Evaluates policies for any combination of actor + action + resource context.
    
    Policy Resolution Order:
      1. Explicit DENY rules (highest priority)
      2. Classification ceiling check
      3. Role-based allow rules
      4. Department-based allow rules
      5. Default DENY (Zero-Trust)
    """

    def __init__(self):
        self._policies: Dict[str, EnterprisePolicy] = {}

    def register_policy(self, policy: EnterprisePolicy) -> None:
        self._policies[policy.policy_id] = policy
        logger.info(f"Registered policy '{policy.name}' v{policy.version} [{policy.policy_type}]")

    def get_policies_by_type(self, policy_type: PolicyType) -> List[EnterprisePolicy]:
        return [
            p for p in self._policies.values()
            if p.policy_type == policy_type and p.status == PolicyStatus.PUBLISHED
        ]

    def evaluate(
        self,
        actor_roles: List[str],
        actor_dept: Optional[str],
        action: str,
        resource_classification: ClassificationLevel = ClassificationLevel.INTERNAL,
        resource_dept: Optional[str] = None,
        policy_type: PolicyType = PolicyType.ACCESS
    ) -> PolicyDecision:
        """
        Core policy evaluation method.
        Returns PolicyDecision(granted=True/False, reason=...).
        """
        actor_roles_upper = {r.upper() for r in actor_roles}

        # ── 1. Classification ceiling check ───────────────────────────
        # Determine maximum clearance from roles
        user_clearance = self._resolve_clearance(actor_roles_upper)
        resource_rank = CLASSIFICATION_RANK.get(resource_classification, 0)
        if user_clearance < resource_rank:
            return PolicyDecision(
                granted=False,
                reason=f"Classification ceiling exceeded. Resource is {resource_classification.value}, "
                       f"user clearance allows up to rank {user_clearance}."
            )

        # ── 2. ADMIN bypass ───────────────────────────────────────────
        if "ADMIN" in actor_roles_upper or "SYSTEM" in actor_roles_upper:
            return PolicyDecision(
                granted=True,
                reason="Admin/System actor — policy bypass granted."
            )

        # ── 3. Evaluate published ACCESS policies ────────────────────
        applicable_policies = self.get_policies_by_type(policy_type)
        for policy in applicable_policies:
            decision = self._evaluate_single(policy, actor_roles_upper, actor_dept, action, resource_dept)
            if decision is not None:
                return decision

        # ── 4. Default: Zero-Trust DENY ───────────────────────────────
        # If no published policy explicitly grants access, deny.
        # In development/bootstrap mode, allow if no policies are registered.
        if not applicable_policies:
            logger.debug(f"No published {policy_type} policies found — Zero-Trust bootstrap allow for '{action}'")
            return PolicyDecision(granted=True, reason="No policies registered — bootstrap allow.")

        return PolicyDecision(
            granted=False,
            reason=f"No policy grants '{action}' to roles {actor_roles_upper}."
        )

    def _evaluate_single(
        self,
        policy: EnterprisePolicy,
        actor_roles: set,
        actor_dept: Optional[str],
        action: str,
        resource_dept: Optional[str]
    ) -> Optional[PolicyDecision]:
        """Evaluates a single policy. Returns decision or None if not applicable."""
        # Role scope check
        if policy.applies_to_roles and not (actor_roles & set(r.upper() for r in policy.applies_to_roles)):
            return None  # Policy not applicable to this actor

        # Dept scope check
        if policy.applies_to_depts and actor_dept and actor_dept not in policy.applies_to_depts:
            return None

        for rule in policy.rules:
            rule_action = rule.get("action", "*")
            if rule_action != "*" and rule_action != action:
                continue

            effect = rule.get("effect", "DENY").upper()
            conditions = rule.get("conditions", [])

            # Evaluate rule conditions
            cond_met = self._evaluate_conditions(conditions, actor_roles, actor_dept, resource_dept)
            if cond_met:
                return PolicyDecision(
                    granted=(effect == "ALLOW"),
                    policy_id=policy.policy_id,
                    reason=f"Policy '{policy.name}' rule: {effect} on action '{action}'",
                    conditions=conditions
                )

        return None

    def _evaluate_conditions(
        self,
        conditions: List[str],
        actor_roles: set,
        actor_dept: Optional[str],
        resource_dept: Optional[str]
    ) -> bool:
        """Evaluates a list of condition strings. All must be satisfied."""
        for condition in conditions:
            if condition == "SAME_DEPARTMENT":
                if actor_dept and resource_dept and actor_dept != resource_dept:
                    return False
            elif condition.startswith("ROLE:"):
                required_role = condition[5:].upper()
                if required_role not in actor_roles:
                    return False
        return True

    def _resolve_clearance(self, roles: set) -> int:
        """Maps roles to a maximum classification clearance rank."""
        ROLE_CLEARANCE = {
            "ADMIN": 6,
            "SECURITY_OFFICER": 6,
            "KNOWLEDGE_MANAGER": 4,
            "MANAGER": 3,
            "SUPERVISOR": 2,
            "USER": 1,
            "VIEWER": 0,
        }
        return max((ROLE_CLEARANCE.get(r, 1) for r in roles), default=1)
