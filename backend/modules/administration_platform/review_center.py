"""
Master Editor & Review Center (EP-13).
Centralized aggregation of all Governance review packages for Administrative approval.
"""
import logging
from typing import List, Dict, Optional

from .models import ReviewQueueItem, ReviewStatus
from modules.governance_platform.governance_engine import GovernanceEngine

logger = logging.getLogger("Administration.ReviewCenter")


class ReviewCenter:
    def __init__(self, gov_engine: GovernanceEngine):
        self._gov_engine = gov_engine
        self._queue: Dict[str, ReviewQueueItem] = {}

    def fetch_upstream_packages(self) -> None:
        """
        Pulls PENDING packages from the core GovernanceEngine and maps them 
        into the unified UI ReviewQueueItem model if they aren't already tracked.
        """
        gov_packages = self._gov_engine.get_pending_reviews()
        for pkg in gov_packages:
            if not any(i.governance_package_id == pkg.package_id for i in self._queue.values()):
                # Create wrapper
                item = ReviewQueueItem(
                    governance_package_id=pkg.package_id,
                    action_type=pkg.change_type.value,
                    requested_by=pkg.proposed_by,
                    impact_summary=pkg.impact_analysis
                )
                self._queue[item.queue_id] = item
                logger.debug(f"Imported Governance package {pkg.package_id} to Admin Queue as {item.queue_id}")

    def get_queue(self, status: Optional[ReviewStatus] = None) -> List[ReviewQueueItem]:
        """Returns the current review queue, optionally filtered by status."""
        self.fetch_upstream_packages()
        items = list(self._queue.values())
        if status:
            items = [i for i in items if i.status == status]
        # Sort newest first
        return sorted(items, key=lambda i: i.created_at, reverse=True)

    def process_review(self, queue_id: str, action: str, reviewer: str, notes: str = "") -> ReviewQueueItem:
        """Approves or Rejects an item in the queue, pushing the result to Governance."""
        from datetime import datetime, timezone
        item = self._queue.get(queue_id)
        if not item:
            raise ValueError(f"Queue item {queue_id} not found.")

        if action.upper() == "APPROVE":
            item.status = ReviewStatus.APPROVED
            self._gov_engine.approve_change(item.governance_package_id, reviewer)
        elif action.upper() == "REJECT":
            item.status = ReviewStatus.REJECTED
            self._gov_engine.reject_change(item.governance_package_id, reviewer, notes)
        else:
            raise ValueError(f"Unknown review action: {action}")

        item.reviewed_by = reviewer
        item.review_notes = notes
        item.reviewed_at = datetime.now(timezone.utc)
        
        logger.info(f"Review item {queue_id} {item.status.value} by {reviewer}")
        return item
