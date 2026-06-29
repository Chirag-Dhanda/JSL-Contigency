"""
Notification Framework for Enterprise Workflow (EP-07).
Generates metadata-driven in-app notifications from workflow events.

Future Extension Points:
  - Email: hook `send_email_notification()`
  - MS Teams / Slack: hook `send_teams_notification()`
  - SAP Events: hook `emit_sap_event()`
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from .models import WorkflowEvent
from .events import EventEngine, EventTypes

logger = logging.getLogger("WorkflowEngine.Notifications")


@dataclass
class Notification:
    id: str
    recipient_id: str
    subject: str
    body: str
    notification_type: str = "IN_APP"  # IN_APP | EMAIL (future) | TEAMS (future)
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    read: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class NotificationInbox:
    """
    In-memory in-app notification store.
    Future: Replace with a DB table (DbNotification) for persistence and push delivery.
    """

    def __init__(self):
        self._inbox: List[Notification] = []

    def push(self, notification: Notification) -> None:
        self._inbox.append(notification)
        logger.info(f"[Notification] -> {notification.recipient_id}: {notification.subject}")

    def get_for_user(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        result = [n for n in self._inbox if n.recipient_id == user_id]
        if unread_only:
            result = [n for n in result if not n.read]
        return result

    def mark_read(self, notification_id: str) -> None:
        for n in self._inbox:
            if n.id == notification_id:
                n.read = True


class NotificationFramework:
    """
    Subscribes to the EventEngine and converts events into Notifications.
    Uses metadata-driven templates (stored as strings for EP-07; future: DB templates).
    """

    TEMPLATES = {
        EventTypes.TASK_CREATED: {
            "subject": "New Task Assigned: {task_title}",
            "body": "You have been assigned a new task: '{task_title}' on workflow instance {instance_id}."
        },
        EventTypes.APPROVAL_REQUESTED: {
            "subject": "Approval Required",
            "body": "Your approval is required on workflow instance {instance_id}. Please review and take action."
        },
        EventTypes.WORKFLOW_COMPLETED: {
            "subject": "Workflow Completed",
            "body": "Workflow instance {instance_id} has completed successfully."
        },
        EventTypes.APPROVAL_REJECTED: {
            "subject": "Approval Rejected",
            "body": "Your submission was rejected on workflow {instance_id}. Comments: {comments}"
        }
    }

    def __init__(self, inbox: NotificationInbox, event_engine: EventEngine):
        self.inbox = inbox
        self._register_handlers(event_engine)

    def _register_handlers(self, event_engine: EventEngine) -> None:
        event_engine.subscribe(EventTypes.TASK_CREATED, self._on_task_created)
        event_engine.subscribe(EventTypes.APPROVAL_REQUESTED, self._on_approval_requested)
        event_engine.subscribe(EventTypes.WORKFLOW_COMPLETED, self._on_workflow_completed)
        event_engine.subscribe(EventTypes.APPROVAL_REJECTED, self._on_approval_rejected)

    def _render(self, event_type: str, payload: dict) -> tuple[str, str]:
        tmpl = self.TEMPLATES.get(event_type, {
            "subject": f"Workflow Event: {event_type}",
            "body": str(payload)
        })
        subject = tmpl["subject"].format_map(payload)
        body = tmpl["body"].format_map(payload)
        return subject, body

    async def _on_task_created(self, event: WorkflowEvent) -> None:
        owner = event.payload.get("owner")
        if not owner:
            return
        subject, body = self._render(EventTypes.TASK_CREATED, {
            "task_title": event.payload.get("task_title", "Untitled"),
            "instance_id": event.entity_id or "unknown"
        })
        self.inbox.push(Notification(
            id=f"notif-task-{event.entity_id}",
            recipient_id=owner,
            subject=subject,
            body=body,
            entity_type="workflow_instance",
            entity_id=event.entity_id
        ))

    async def _on_approval_requested(self, event: WorkflowEvent) -> None:
        approver = event.payload.get("approver")
        if not approver:
            return
        subject, body = self._render(EventTypes.APPROVAL_REQUESTED, {
            "instance_id": event.entity_id or "unknown"
        })
        self.inbox.push(Notification(
            id=f"notif-approval-{event.entity_id}",
            recipient_id=approver,
            subject=subject,
            body=body,
            entity_type="workflow_instance",
            entity_id=event.entity_id
        ))

    async def _on_workflow_completed(self, event: WorkflowEvent) -> None:
        initiator = event.payload.get("started_by")
        if not initiator:
            return
        subject, body = self._render(EventTypes.WORKFLOW_COMPLETED, {
            "instance_id": event.entity_id or "unknown"
        })
        self.inbox.push(Notification(
            id=f"notif-complete-{event.entity_id}",
            recipient_id=initiator,
            subject=subject,
            body=body,
            entity_type="workflow_instance",
            entity_id=event.entity_id
        ))

    async def _on_approval_rejected(self, event: WorkflowEvent) -> None:
        initiator = event.payload.get("started_by")
        if not initiator:
            return
        subject, body = self._render(EventTypes.APPROVAL_REJECTED, {
            "instance_id": event.entity_id or "unknown",
            "comments": event.payload.get("comments", "No comments provided.")
        })
        self.inbox.push(Notification(
            id=f"notif-rejected-{event.entity_id}",
            recipient_id=initiator,
            subject=subject,
            body=body,
            entity_type="workflow_instance",
            entity_id=event.entity_id
        ))
