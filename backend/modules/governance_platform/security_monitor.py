"""
Security Monitor (EP-09).
Records and analyzes security events for anomalous behavior.
"""
import logging
from typing import List, Dict, Any, Optional

from .models import SecurityEvent, SecurityEventType

logger = logging.getLogger("Governance.SecurityMonitor")


class SecurityMonitor:
    def __init__(self):
        self._events: List[SecurityEvent] = []

    def record_event(
        self,
        event_type: SecurityEventType,
        actor_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "INFO"
    ) -> SecurityEvent:
        event = SecurityEvent(
            event_type=event_type,
            severity=severity,
            actor_id=actor_id,
            resource_id=resource_id,
            resource_type=resource_type,
            details=details or {}
        )
        self._events.append(event)
        
        log_msg = f"[SEC] {event_type.value} | Actor: {actor_id} | Resource: {resource_id}"
        if severity == "CRITICAL":
            logger.error(log_msg)
        elif severity == "WARN":
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
            
        return event

    def get_events(self, limit: int = 100) -> List[SecurityEvent]:
        # Return most recent first
        return sorted(self._events, key=lambda e: e.timestamp, reverse=True)[:limit]

    def get_analytics(self) -> Dict[str, Any]:
        """Summarize security events."""
        total = len(self._events)
        if total == 0:
            return {"total_events": 0}

        counts_by_type = {}
        for e in self._events:
            counts_by_type[e.event_type.value] = counts_by_type.get(e.event_type.value, 0) + 1

        failures = counts_by_type.get(SecurityEventType.AUTH_FAILURE.value, 0)
        denies = counts_by_type.get(SecurityEventType.AUTHZ_DENIED.value, 0)
        ai_blocks = counts_by_type.get(SecurityEventType.AI_PERMISSION_BLOCK.value, 0)
        
        return {
            "total_events": total,
            "counts_by_type": counts_by_type,
            "metrics": {
                "auth_failures": failures,
                "authorization_denials": denies,
                "ai_blocks": ai_blocks
            }
        }
