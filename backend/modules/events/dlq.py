"""
Dead Letter Queue Manager (EP-11).
"""
import logging
from typing import List, Dict, Optional

from .models import DLQRecord, DomainEvent

logger = logging.getLogger("Event.DLQ")


class IDLQStorage:
    def add(self, record: DLQRecord) -> None:
        raise NotImplementedError
        
    def get_all_unresolved(self) -> List[DLQRecord]:
        raise NotImplementedError
        
    def get_by_id(self, dlq_id: str) -> Optional[DLQRecord]:
        raise NotImplementedError


class InMemoryDLQ(IDLQStorage):
    def __init__(self):
        self._records: Dict[str, DLQRecord] = {}

    def add(self, record: DLQRecord) -> None:
        self._records[record.dlq_id] = record
        logger.error(
            f"DLQ ENTRY [{record.dlq_id}]: Event {record.event.event_type} "
            f"failed for subscriber '{record.subscriber_name}'. Error: {record.error_message}"
        )

    def get_all_unresolved(self) -> List[DLQRecord]:
        return [r for r in self._records.values() if r.status in ("FAILED", "RETRYING")]
        
    def get_by_id(self, dlq_id: str) -> Optional[DLQRecord]:
        return self._records.get(dlq_id)

    def update_status(self, dlq_id: str, status: str) -> None:
        record = self._records.get(dlq_id)
        if record:
            record.status = status
            logger.info(f"DLQ Record {dlq_id} marked as {status}")
