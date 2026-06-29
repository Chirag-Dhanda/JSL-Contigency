"""
API Router for Enterprise Workflow & Process Orchestration Engine (EP-07).
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form, Query

from core.di import container
from modules.auth.middleware import require_authenticated_user
from .models import WorkflowDefinitionMeta, WorkflowInstanceModel, WorkflowTaskModel, WorkflowApprovalModel
from .definition import WorkflowDefinitionService
from .runtime import WorkflowRuntimeEngine
from .task_engine import TaskManagementService
from .approval_engine import ApprovalEngineService
from .notifications import NotificationInbox, Notification

logger = logging.getLogger("WorkflowEngine.API")
router = APIRouter(prefix="/api/v1/workflows", tags=["Enterprise Workflow Engine"])


# ─────────────────────────────────────────────
# Workflow Definitions
# ─────────────────────────────────────────────

@router.post("/definitions", response_model=WorkflowDefinitionMeta)
async def create_workflow_definition(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    states: str = Form(..., description="JSON array of WorkflowState objects"),
    transitions: str = Form(..., description="JSON array of WorkflowTransition objects"),
    definition_svc: WorkflowDefinitionService = Depends(lambda: container.resolve(WorkflowDefinitionService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Creates a new workflow definition as DRAFT."""
    import json
    payload = {
        "states": json.loads(states),
        "transitions": json.loads(transitions)
    }
    return await definition_svc.create_draft(
        name=name,
        definition_payload=payload,
        created_by=auth_context.get("sub", "system"),
        description=description
    )


@router.post("/definitions/{workflow_id}/publish", response_model=WorkflowDefinitionMeta)
async def publish_workflow_definition(
    workflow_id: str,
    definition_svc: WorkflowDefinitionService = Depends(lambda: container.resolve(WorkflowDefinitionService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Publishes a workflow definition, allowing instances to be created."""
    try:
        return await definition_svc.publish_workflow(workflow_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─────────────────────────────────────────────
# Workflow Instances (Runtime)
# ─────────────────────────────────────────────

@router.post("/instances", response_model=WorkflowInstanceModel)
async def start_workflow_instance(
    workflow_name: str = Form(...),
    target_entity_id: Optional[str] = Form(None),
    target_entity_type: Optional[str] = Form(None),
    runtime: WorkflowRuntimeEngine = Depends(lambda: container.resolve(WorkflowRuntimeEngine)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Starts a new instance of the latest published workflow by name."""
    try:
        return await runtime.start_workflow(
            workflow_name=workflow_name,
            started_by=auth_context.get("sub", "system"),
            target_entity_id=target_entity_id,
            target_entity_type=target_entity_type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/instances/{instance_id}/advance", response_model=WorkflowInstanceModel)
async def advance_workflow_state(
    instance_id: str,
    trigger_event: str = Form(...),
    runtime: WorkflowRuntimeEngine = Depends(lambda: container.resolve(WorkflowRuntimeEngine)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Trigger a state transition on a running workflow instance."""
    try:
        return await runtime.advance_state(
            instance_id=instance_id,
            trigger_event=trigger_event,
            actor_id=auth_context.get("sub", "system")
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────

@router.post("/tasks", response_model=WorkflowTaskModel)
async def create_task(
    instance_id: str = Form(...),
    title: str = Form(...),
    owner_id: str = Form(...),
    department_id: Optional[str] = Form(None),
    task_svc: TaskManagementService = Depends(lambda: container.resolve(TaskManagementService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    return await task_svc.create_task(instance_id, title, owner_id, department_id)


@router.post("/tasks/{task_id}/complete", response_model=WorkflowTaskModel)
async def complete_task(
    task_id: str,
    task_svc: TaskManagementService = Depends(lambda: container.resolve(TaskManagementService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    try:
        return await task_svc.complete_task(task_id, auth_context.get("sub", "system"))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─────────────────────────────────────────────
# Approvals
# ─────────────────────────────────────────────

@router.post("/approvals/request", response_model=WorkflowApprovalModel)
async def request_approval(
    instance_id: str = Form(...),
    approver_id: str = Form(...),
    approver_department: str = Form(...),
    approval_svc: ApprovalEngineService = Depends(lambda: container.resolve(ApprovalEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    return await approval_svc.request_approval(instance_id, approver_id, approver_department)


@router.post("/approvals/{approval_id}/decide", response_model=WorkflowApprovalModel)
async def record_approval_decision(
    approval_id: str,
    decision: str = Form(..., description="APPROVED or REJECTED"),
    comments: Optional[str] = Form(None),
    approval_svc: ApprovalEngineService = Depends(lambda: container.resolve(ApprovalEngineService)),
    auth_context: dict = Depends(require_authenticated_user)
):
    try:
        return await approval_svc.record_decision(approval_id, auth_context.get("sub", "system"), decision, comments)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# Notifications
# ─────────────────────────────────────────────

@router.get("/notifications/me")
async def get_my_notifications(
    unread_only: bool = Query(False),
    inbox: NotificationInbox = Depends(lambda: container.resolve(NotificationInbox)),
    auth_context: dict = Depends(require_authenticated_user)
):
    """Returns in-app notifications for the authenticated user."""
    user_id = auth_context.get("sub", "system")
    notifications = inbox.get_for_user(user_id, unread_only=unread_only)
    return [{"id": n.id, "subject": n.subject, "body": n.body, "read": n.read, "created_at": n.created_at} for n in notifications]
