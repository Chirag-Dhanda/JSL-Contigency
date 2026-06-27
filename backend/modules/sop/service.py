from typing import Dict, List, Optional
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import SOPDocument, SOPSection, SOPMetadata, SOPWorkflowStep
from .enums import SOPStatus, WorkflowRole

logger = getLogger("SOPEngine")

class SOPEngine:
    def __init__(self):
        self._sops: Dict[str, SOPDocument] = {}

    def create_draft(self, title: str, department_id: str, category: str, author_id: str) -> SOPDocument:
        now = datetime.now(timezone.utc)
        sop = SOPDocument(
            id=str(uuid.uuid4()),
            title=title,
            department_id=department_id,
            category=category,
            status=SOPStatus.DRAFT,
            metadata=SOPMetadata(
                sop_number=f"SOP-{str(uuid.uuid4())[:8].upper()}",
                revision_number=0,
                version="1.0.0",
                author_id=author_id,
                created_at=now,
                last_updated=now
            )
        )
        self._sops[sop.id] = sop
        logger.info(f"Created new SOP draft: {title} ({sop.metadata.sop_number})")
        return sop

    def add_section(self, sop_id: str, title: str, content: str) -> SOPDocument:
        sop = self._sops.get(sop_id)
        if not sop:
            raise ValueError("SOP not found")
        
        section = SOPSection(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            order_index=len(sop.sections)
        )
        sop.sections.append(section)
        sop.metadata.last_updated = datetime.now(timezone.utc)
        return sop

    def submit_for_review(self, sop_id: str, workflow_steps: List[WorkflowRole]) -> SOPDocument:
        sop = self._sops.get(sop_id)
        if not sop or sop.status != SOPStatus.DRAFT:
            raise ValueError("Invalid SOP or not in DRAFT status.")

        sop.status = SOPStatus.UNDER_REVIEW
        sop.active_workflow_state = [SOPWorkflowStep(role=role) for role in workflow_steps]
        logger.info(f"SOP {sop_id} submitted for review.")
        return sop

    def publish_sop(self, sop_id: str) -> SOPDocument:
        sop = self._sops.get(sop_id)
        if not sop or sop.status != SOPStatus.UNDER_REVIEW:
            raise ValueError("Only SOPs UNDER_REVIEW can be published (assuming all steps approved).")

        sop.status = SOPStatus.PUBLISHED
        now = datetime.now(timezone.utc)
        sop.metadata.effective_date = now
        sop.metadata.last_updated = now
        
        # In a real system, we would search for older versions and mark them SUPERSEDED
        
        logger.info(f"SOP {sop_id} PUBLISHED (v{sop.metadata.version})")
        return sop

    def get_sop(self, sop_id: str) -> Optional[SOPDocument]:
        return self._sops.get(sop_id)
        
    def search_sops(self, keyword: str = "", department_id: str = "") -> List[SOPDocument]:
        results = []
        for sop in self._sops.values():
            if keyword and keyword.lower() not in sop.title.lower():
                continue
            if department_id and sop.department_id != department_id:
                continue
            results.append(sop)
        return results
