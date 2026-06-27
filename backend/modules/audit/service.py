from .models import AuditEvent
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from logging import getLogger
import uuid

logger = getLogger("AuditService")

class AuditService:
    """Centralized immutable ledger for enterprise compliance."""
    
    def __init__(self):
        # In-memory storage for functional testing
        self._ledger: list[AuditEvent] = []
        
    async def log_event(self, action: str, actor_id: str, target_resource_id: Optional[str] = None, metadata: Dict[str, Any] = None) -> None:
        event = AuditEvent(
            id=str(uuid.uuid4()),
            action=action,
            actor_id=actor_id,
            target_resource_id=target_resource_id,
            timestamp=datetime.now(timezone.utc),
            metadata_snapshot=metadata or {}
        )
        self._ledger.append(event)
        logger.info(f"AUDIT LOG: {action} by {actor_id} targeting {target_resource_id}")
        
    async def get_events_for_resource(self, target_resource_id: str) -> list[AuditEvent]:
        return [e for e in self._ledger if e.target_resource_id == target_resource_id]
