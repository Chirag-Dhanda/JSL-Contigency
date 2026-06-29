"""
Metadata-driven Subscription Engine (EP-11).
Allows dynamic registration of event handlers without hardcoding them at boot.
"""
import logging
from typing import Dict, List, Any

from .models import SubscriptionRule, DomainEvent
from .bus import AdvancedEventBus

logger = logging.getLogger("Event.SubscriptionEngine")


class SubscriptionEngine:
    def __init__(self, bus: AdvancedEventBus):
        self._bus = bus
        self._rules: Dict[str, SubscriptionRule] = {}

    def register_rule(self, rule: SubscriptionRule, handler_ref: Any) -> None:
        """
        Registers a dynamic subscription rule and binds it to a handler reference.
        """
        self._rules[rule.subscription_id] = rule
        
        if rule.is_active:
            # Wrap the handler to evaluate filter conditions before executing
            async def _filtered_handler(event: DomainEvent):
                if self._evaluate_filters(event.payload, rule.filter_conditions):
                    await handler_ref(event)
                else:
                    logger.debug(f"Event {event.event_id} filtered out for {rule.subscriber_name}")
                    
            self._bus.subscribe(rule.event_type, rule.subscriber_name, _filtered_handler)
            logger.info(f"Registered dynamic subscription: {rule.subscriber_name} -> {rule.event_type}")

    def _evaluate_filters(self, payload: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Evaluates simple key-value equality filters."""
        if not filters:
            return True
            
        for key, expected_val in filters.items():
            if payload.get(key) != expected_val:
                return False
        return True
