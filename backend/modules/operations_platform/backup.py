"""
Backup & Recovery Framework (EP-12).
Orchestrates backups and enforces governance on restore operations.
"""
import logging
from typing import List, Dict, Optional

from .models import BackupRecord, OperationsReviewPackage
from modules.governance_platform.governance_engine import GovernanceEngine
from modules.governance_platform.models import GovernanceChangeType

logger = logging.getLogger("Operations.Backup")


class BackupManager:
    def __init__(self, gov_engine: GovernanceEngine):
        self._gov_engine = gov_engine
        self._backups: Dict[str, BackupRecord] = {}

    def initiate_backup(self, component: str) -> BackupRecord:
        """
        Records metadata for a new backup operation.
        The actual backup execution (e.g., pg_dump) is orchestrated asynchronously.
        """
        record = BackupRecord(component=component)
        self._backups[record.backup_id] = record
        
        logger.info(f"Initiated backup for {component}. ID: {record.backup_id}")
        
        # Simulate immediate success for the mock
        from datetime import datetime, timezone
        record.status = "SUCCESS"
        record.completed_at = datetime.now(timezone.utc)
        record.size_bytes = 104857600  # 100MB
        record.location_uri = f"s3://ekos-backups/{component}/{record.backup_id}.tar.gz"
        
        return record

    def get_backups(self) -> List[BackupRecord]:
        return list(self._backups.values())

    # ── Operational Automation (Restore) ────────────────────────────────────────

    def propose_restore(self, backup_id: str, requested_by: str) -> str:
        """
        Restoring from backup is highly destructive to current state.
        It must be approved by an administrator via the Governance Engine.
        """
        record = self._backups.get(backup_id)
        if not record:
            raise ValueError(f"Backup {backup_id} not found.")

        gov_pkg = self._gov_engine.propose_change(
            change_type=GovernanceChangeType.GOVERNANCE_RULE_CHANGE, # Mapping to closest enum
            proposed_by=requested_by,
            description=f"RESTORE DATA FROM BACKUP: {backup_id}",
            proposed_state={"action": "RESTORE", "backup_id": backup_id, "component": record.component},
            impact_analysis=f"Will overwrite current {record.component} state with data from {record.started_at}. All intervening data will be lost."
        )
        
        logger.warning(f"Restore proposed for backup {backup_id}. Awaiting admin approval (Package: {gov_pkg.package_id}).")
        return gov_pkg.package_id
