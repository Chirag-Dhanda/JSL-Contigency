"""
Compliance Framework (EP-09).
Manages metadata for industry compliance (ISO, SOC2, GDPR, etc).
"""
import logging
from typing import List, Dict, Optional

from .models import ComplianceRecord, ComplianceStandard

logger = logging.getLogger("Governance.Compliance")


class ComplianceFramework:
    def __init__(self):
        self._records: Dict[str, ComplianceRecord] = {}

    def add_record(self, record: ComplianceRecord) -> None:
        self._records[record.record_id] = record
        logger.info(f"Added compliance record: {record.standard.value} - {record.control_id}")

    def get_records(self, standard: Optional[str] = None) -> List[ComplianceRecord]:
        if standard:
            return [r for r in self._records.values() if r.standard.value == standard]
        return list(self._records.values())

    def update_status(self, record_id: str, status: str) -> None:
        record = self._records.get(record_id)
        if record:
            record.status = status
            from datetime import datetime, timezone
            record.last_reviewed = datetime.now(timezone.utc)
            logger.info(f"Updated compliance record '{record_id}' to status '{status}'")
