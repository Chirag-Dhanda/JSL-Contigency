from typing import Dict, Optional, List
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import ContentItem, VersionInfo, ApprovalWorkflow, ChangeLog, ApprovalStep
from .enums import ContentStatus

logger = getLogger("LCMSEngine")

class LCMSEngine:
    def __init__(self):
        self._content: Dict[str, ContentItem] = {}
        self._workflows: Dict[str, ApprovalWorkflow] = {}

    def register_workflow(self, workflow: ApprovalWorkflow):
        self._workflows[workflow.id] = workflow
        logger.info(f"Registered workflow template: {workflow.name}")

    def create_draft(self, title: str, description: str, payload_ref_id: str, author_id: str) -> ContentItem:
        now = datetime.now(timezone.utc)
        item = ContentItem(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            payload_ref_id=payload_ref_id,
            status=ContentStatus.DRAFT,
            version_info=VersionInfo(
                author_id=author_id,
                created_at=now,
                last_updated=now,
                change_history=[ChangeLog(changed_by_user_id=author_id, change_description="Initial Draft", timestamp=now)]
            )
        )
        self._content[item.id] = item
        logger.info(f"Created new draft: {title} ({item.id})")
        return item

    def submit_for_review(self, content_id: str, workflow_id: str) -> ContentItem:
        item = self._content.get(content_id)
        workflow = self._workflows.get(workflow_id)
        if not item or not workflow:
            raise ValueError("Item or Workflow not found.")
            
        if item.status != ContentStatus.DRAFT:
            raise ValueError("Only DRAFT items can be submitted for review.")

        item.status = ContentStatus.UNDER_REVIEW
        item.active_workflow_id = workflow.id
        # Clone steps from template to maintain state
        item.active_workflow_state = [ApprovalStep(**step.model_dump()) for step in workflow.steps]
        
        logger.info(f"Item {content_id} submitted for review using workflow {workflow.name}")
        return item

    def process_approval(self, content_id: str, approver_id: str, is_approved: bool, comments: str = "") -> ContentItem:
        item = self._content.get(content_id)
        if not item or item.status != ContentStatus.UNDER_REVIEW:
            raise ValueError("Invalid item or not under review.")

        for step in item.active_workflow_state:
            if step.status == "PENDING":
                step.status = "APPROVED" if is_approved else "REJECTED"
                step.approved_by_user_id = approver_id
                step.timestamp = datetime.now(timezone.utc)
                step.comments = comments
                
                logger.info(f"Approval step {step.role.value} processed as {step.status} for item {content_id}")
                
                if not is_approved:
                    item.status = ContentStatus.DRAFT # Kick back to draft
                    item.active_workflow_state = []
                    logger.warning(f"Item {content_id} rejected. Kicked back to draft.")
                    return item
                break

        # Check if all steps approved
        all_approved = all(s.status == "APPROVED" for s in item.active_workflow_state)
        if all_approved:
            item.status = ContentStatus.APPROVED
            logger.info(f"Item {content_id} fully APPROVED.")
            
        return item

    def publish_content(self, content_id: str, publisher_id: str) -> ContentItem:
        item = self._content.get(content_id)
        if not item or item.status != ContentStatus.APPROVED:
            raise ValueError("Only APPROVED items can be published.")

        item.status = ContentStatus.PUBLISHED
        item.version_info.published_at = datetime.now(timezone.utc)
        item.version_info.change_history.append(
            ChangeLog(changed_by_user_id=publisher_id, change_description="Published Content", timestamp=item.version_info.published_at)
        )
        logger.info(f"Item {content_id} PUBLISHED (v{item.version_info.version_string})")
        return item

    def create_new_version(self, content_id: str, author_id: str, bump_type: str = "minor") -> ContentItem:
        """Bumps version and sets back to DRAFT state."""
        item = self._content.get(content_id)
        if not item:
            raise ValueError("Item not found.")
            
        now = datetime.now(timezone.utc)
        
        if bump_type == "major":
            item.version_info.major += 1
            item.version_info.minor = 0
            item.version_info.patch = 0
        elif bump_type == "minor":
            item.version_info.minor += 1
            item.version_info.patch = 0
        else:
            item.version_info.patch += 1
            
        item.status = ContentStatus.DRAFT
        item.active_workflow_state = []
        item.version_info.last_updated = now
        item.version_info.change_history.append(
            ChangeLog(changed_by_user_id=author_id, change_description=f"Bumped version to {item.version_info.version_string}", timestamp=now)
        )
        
        logger.info(f"Item {content_id} bumped to v{item.version_info.version_string}")
        return item
