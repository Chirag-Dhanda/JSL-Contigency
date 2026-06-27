from typing import Dict, Optional
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import ProgressRecord, EntityType, ProgressStatus

logger = getLogger("ProgressEngine")

class ProgressEngine:
    def __init__(self):
        # Keyed by f"{user_id}:{entity_id}"
        self._records: Dict[str, ProgressRecord] = {}

    def get_progress(self, user_id: str, entity_id: str) -> Optional[ProgressRecord]:
        return self._records.get(f"{user_id}:{entity_id}")

    def init_progress(self, user_id: str, entity_id: str, entity_type: EntityType) -> ProgressRecord:
        key = f"{user_id}:{entity_id}"
        if key not in self._records:
            self._records[key] = ProgressRecord(
                id=str(uuid.uuid4()),
                user_id=user_id,
                entity_id=entity_id,
                entity_type=entity_type,
                last_accessed=datetime.now(timezone.utc)
            )
            logger.info(f"Initialized progress tracking for User {user_id} on {entity_type.value} {entity_id}")
        return self._records[key]

    def update_progress(self, user_id: str, entity_id: str, completion_percentage: float, time_spent_mins: int = 0) -> ProgressRecord:
        key = f"{user_id}:{entity_id}"
        record = self._records.get(key)
        if not record:
            raise ValueError("Progress record not found. Initialize first.")

        record.completion_percentage = min(100.0, max(0.0, completion_percentage))
        record.time_spent_mins += time_spent_mins
        
        # Simple moving average for session mins mock
        record.average_session_mins = (record.average_session_mins + time_spent_mins) / 2 if record.average_session_mins > 0 else time_spent_mins

        record.last_accessed = datetime.now(timezone.utc)
        
        if record.status == ProgressStatus.NOT_STARTED and completion_percentage > 0:
            record.status = ProgressStatus.IN_PROGRESS
            
        if completion_percentage == 100.0:
            record.status = ProgressStatus.COMPLETED
            record.completed_at = datetime.now(timezone.utc)
            
        self._records[key] = record
        logger.debug(f"Updated progress to {completion_percentage}% for User {user_id} on Entity {entity_id}")
        return record
