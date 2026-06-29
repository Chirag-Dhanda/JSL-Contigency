"""
Enterprise Governance Engine (EP-09).
Manages Human-in-the-Loop review packages for governance changes.
"""
import logging
from typing import Dict, List, Any, Optional

from .models import GovernanceReviewPackage, GovernanceChangeType, GovernanceReviewStatus
from .security_monitor import SecurityMonitor, SecurityEventType

logger = logging.getLogger("Governance.Engine")


class GovernanceEngine:
    def __init__(self, security_monitor: SecurityMonitor):
        self._packages: Dict[str, GovernanceReviewPackage] = {}
        self._monitor = security_monitor

    def propose_change(
        self,
        change_type: GovernanceChangeType,
        proposed_by: str,
        description: str,
        proposed_state: Dict[str, Any],
        current_state: Optional[Dict[str, Any]] = None,
        impact_analysis: str = ""
    ) -> GovernanceReviewPackage:
        """Creates a governance package for review."""
        package = GovernanceReviewPackage(
            change_type=change_type,
            proposed_by=proposed_by,
            description=description,
            current_state=current_state,
            proposed_state=proposed_state,
            impact_analysis=impact_analysis
        )
        self._packages[package.package_id] = package
        logger.info(f"Proposed governance change '{package.package_id}' ({change_type.value}) by {proposed_by}")
        return package

    def approve_change(self, package_id: str, approver_id: str) -> GovernanceReviewPackage:
        package = self._packages.get(package_id)
        if not package:
            raise ValueError(f"Governance package '{package_id}' not found.")
        
        if package.status != GovernanceReviewStatus.PENDING:
            raise ValueError(f"Package '{package_id}' is already {package.status.value}")

        package.status = GovernanceReviewStatus.APPROVED
        package.reviewed_by = approver_id
        from datetime import datetime, timezone
        package.reviewed_at = datetime.now(timezone.utc)
        
        logger.info(f"Governance package '{package_id}' APPROVED by {approver_id}")
        
        # Log to security monitor
        self._monitor.record_event(
            event_type=SecurityEventType.GOVERNANCE_CHANGE,
            actor_id=approver_id,
            details={"package_id": package_id, "action": "APPROVED", "change_type": package.change_type.value},
            severity="WARN"  # Governance changes are significant
        )
        return package

    def reject_change(self, package_id: str, approver_id: str, reason: str) -> GovernanceReviewPackage:
        package = self._packages.get(package_id)
        if not package:
            raise ValueError(f"Governance package '{package_id}' not found.")
            
        package.status = GovernanceReviewStatus.REJECTED
        package.reviewed_by = approver_id
        package.review_notes = reason
        from datetime import datetime, timezone
        package.reviewed_at = datetime.now(timezone.utc)
        
        logger.info(f"Governance package '{package_id}' REJECTED by {approver_id}. Reason: {reason}")
        return package

    def get_pending_reviews(self) -> List[GovernanceReviewPackage]:
        return [p for p in self._packages.values() if p.status == GovernanceReviewStatus.PENDING]

    def get_package(self, package_id: str) -> Optional[GovernanceReviewPackage]:
        return self._packages.get(package_id)
