"""
Enterprise Audit Platform (EP-09).
Extends existing modules/audit/service.py to a governed, queryable platform capability.
"""
import logging
from typing import List, Dict, Any, Optional

from modules.audit.service import AuditService
from modules.audit.models import AuditEvent

logger = logging.getLogger("Governance.AuditPlatform")


class EnterpriseAuditPlatform:
    """
    Wraps the raw AuditService with a governance-aware API.
    Provides query capabilities, batch exports, and security monitoring integration.
    """

    def __init__(self, raw_audit_service: AuditService):
        self._audit = raw_audit_service

    async def log_event(self, action: str, actor_id: str, target_resource_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        await self._audit.log_event(action, actor_id, target_resource_id, metadata)

    async def get_events_for_resource(self, resource_id: str) -> List[AuditEvent]:
        return await self._audit.get_events_for_resource(resource_id)

    async def query_events(
        self,
        actor_id: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditEvent]:
        """Query the immutable ledger."""
        # For EP-09 (in-memory ledger), we filter the raw list
        results = self._audit._ledger
        
        if actor_id:
            results = [e for e in results if e.actor_id == actor_id]
        if action:
            results = [e for e in results if e.action == action]
            
        return sorted(results, key=lambda e: e.timestamp, reverse=True)[:limit]
