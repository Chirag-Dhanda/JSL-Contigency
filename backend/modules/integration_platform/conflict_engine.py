"""
Conflict Resolution Engine (EP-10).
Detects and parks synchronization conflicts rather than auto-merging destructively.
"""
import logging
from typing import List, Dict, Any, Optional

from .models import ConflictRecord, ConflictType

logger = logging.getLogger("Integration.ConflictEngine")


class ConflictResolutionEngine:
    def __init__(self):
        self._conflicts: Dict[str, ConflictRecord] = {}

    def report_conflict(
        self,
        connector_id: str,
        conflict_type: ConflictType,
        error_message: str,
        external_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None
    ) -> ConflictRecord:
        """
        Registers a conflict that occurred during synchronization.
        """
        record = ConflictRecord(
            connector_id=connector_id,
            conflict_type=conflict_type,
            error_message=error_message,
            external_id=external_id,
            payload=payload or {}
        )
        self._conflicts[record.conflict_id] = record
        
        logger.warning(f"Conflict Detected [{conflict_type.value}] on connector {connector_id}: {error_message}")
        return record

    def get_unresolved_conflicts(self, connector_id: Optional[str] = None) -> List[ConflictRecord]:
        results = [c for c in self._conflicts.values() if not c.resolved]
        if connector_id:
            results = [c for c in results if c.connector_id == connector_id]
        return results

    def resolve_conflict(self, conflict_id: str, resolution_action: str) -> None:
        """
        Mark a conflict as resolved.
        In a real app, `resolution_action` would dictate how to fix the data
        (e.g., 'OVERWRITE_EKOS', 'OVERWRITE_EXTERNAL', 'IGNORE').
        """
        conflict = self._conflicts.get(conflict_id)
        if conflict:
            conflict.resolved = True
            logger.info(f"Resolved conflict {conflict_id} using action: {resolution_action}")
        else:
            raise ValueError(f"Conflict {conflict_id} not found.")
