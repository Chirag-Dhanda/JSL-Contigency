import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

logger = logging.getLogger("EntityVersionManager")

class VersionRecord:
    def __init__(self, version_id: str, version_number: int, changed_by: str, change_summary: str, snapshot: Dict[str, Any]):
        self.version_id = version_id
        self.version_number = version_number
        self.changed_by = changed_by
        self.change_summary = change_summary
        self.timestamp = datetime.now(timezone.utc)
        self.snapshot = snapshot

class VersionTracker:
    """Manages the version history of an enterprise entity."""
    
    def __init__(self):
        self.history: List[VersionRecord] = []
        
    def create_version(self, version_id: str, version_number: int, changed_by: str, change_summary: str, entity_dict: Dict[str, Any]):
        record = VersionRecord(version_id, version_number, changed_by, change_summary, entity_dict)
        self.history.append(record)
        logger.debug(f"Created version v{version_number} with ID: {version_id}")
        
    def get_version(self, version_number: int) -> VersionRecord:
        for record in self.history:
            if record.version_number == version_number:
                return record
        return None
