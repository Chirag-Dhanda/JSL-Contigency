"""
Event-Driven Automation Rules Engine (EP-11).
Executes configured actions based on domain events.
"""
import logging
from typing import Dict, List, Any

from .models import AutomationRule, AutomationActionType, AutomationReviewPackage
from .bus import AdvancedEventBus
from modules.governance_platform.governance_engine import GovernanceEngine
from modules.governance_platform.models import GovernanceChangeType

logger = logging.getLogger("Event.AutomationEngine")


class AutomationEngine:
    def __init__(self, bus: AdvancedEventBus):
        self._bus = bus
        self._rules: Dict[str, AutomationRule] = {}

    @property
    def _gov_engine(self) -> GovernanceEngine:
        from core.di import container
        return container.resolve(GovernanceEngine)

    def register_rule(self, rule: AutomationRule) -> None:
        self._rules[rule.rule_id] = rule
        
        if rule.is_active:
            # Subscribe to the event bus
            self._bus.subscribe(rule.trigger_event_type, f"AutoRule-{rule.name}", self._build_handler(rule))
            logger.info(f"Activated Automation Rule: {rule.name} on {rule.trigger_event_type}")
        else:
            logger.info(f"Registered DRAFT Automation Rule: {rule.name}")

    def _build_handler(self, rule: AutomationRule):
        """Constructs an async handler that evaluates conditions and fires the action."""
        async def _handler(event):
            # 1. Condition Evaluation
            if not self._evaluate_conditions(event.payload, rule.conditions):
                return
                
            logger.info(f"Automation Rule '{rule.name}' triggered by {event.event_id}")
            
            # 2. Action Execution
            if rule.action_type == AutomationActionType.SEND_NOTIFICATION:
                await self._mock_send_notification(rule.action_payload_template, event.payload)
            elif rule.action_type == AutomationActionType.TRIGGER_WORKFLOW:
                await self._mock_trigger_workflow(rule.action_payload_template, event.payload)
            else:
                logger.warning(f"Unsupported Action Type: {rule.action_type}")
                
        return _handler

    def _evaluate_conditions(self, payload: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Evaluates rule conditions against the event payload."""
        for key, expected_val in conditions.items():
            if payload.get(key) != expected_val:
                return False
        return True

    # ── Mock Action Executions ───────────────────────────────────────────────

    async def _mock_send_notification(self, template: Dict, payload: Dict):
        # In reality, this would publish a 'NotificationRequested' event or call a Notification API
        logger.info(f"[ACTION EXECUTION] Sending Notification based on template: {template}")

    async def _mock_trigger_workflow(self, template: Dict, payload: Dict):
        # Calls the Workflow Engine via API or Event
        logger.info(f"[ACTION EXECUTION] Triggering Workflow based on template: {template}")

    # ── Governance Integration ───────────────────────────────────────────────

    def propose_activation(self, rule_id: str, proposed_by: str) -> str:
        """Proposes activating an automation rule via the Governance Engine."""
        rule = self._rules.get(rule_id)
        if not rule:
            raise ValueError(f"Rule {rule_id} not found.")
            
        if not rule.requires_approval:
            rule.is_active = True
            self.register_rule(rule)
            return "AUTO_APPROVED"
            
        gov_pkg = self._gov_engine.propose_change(
            change_type=GovernanceChangeType.GOVERNANCE_RULE_CHANGE,
            proposed_by=proposed_by,
            description=f"Activate Automation Rule: {rule.name}",
            proposed_state={"rule_id": rule_id, "is_active": True},
            impact_analysis=f"Will trigger {rule.action_type.value} automatically on {rule.trigger_event_type}."
        )
        
        logger.info(f"Proposed activation of rule {rule_id}. Package ID: {gov_pkg.package_id}")
        return gov_pkg.package_id
