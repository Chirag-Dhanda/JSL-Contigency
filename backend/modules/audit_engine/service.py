import logging
from typing import List, Dict, Optional
from modules.governance.models import AuditRecord

logger = logging.getLogger("AuditEngine")

class AuditEngineService:
    """
    Immutable ledger for enterprise governance actions.
    """
    def __init__(self):
        self._ledger: List[AuditRecord] = []
        logger.info("Audit Engine Initialized.")

    def record_action(self, user_id: str, entity_id: str, module: str, action: str, old_value: Optional[dict] = None, new_value: Optional[dict] = None, reason: Optional[str] = None) -> AuditRecord:
        record = AuditRecord(
            user_id=user_id,
            entity_id=entity_id,
            module=module,
            action=action,
            old_value=old_value,
            new_value=new_value,
            reason=reason
        )
        self._ledger.append(record)
        logger.info(f"AUDIT [{action}] by {user_id} on {entity_id}")
        return record

    def get_history_for_entity(self, entity_id: str) -> List[AuditRecord]:
        return [r for r in self._ledger if r.entity_id == entity_id]
