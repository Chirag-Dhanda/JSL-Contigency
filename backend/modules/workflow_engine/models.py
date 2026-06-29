"""
Domain models for Enterprise Workflow & Process Orchestration Engine (EP-07).
"""
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# Visual Workflow Metadata Nodes
# ─────────────────────────────────────────────

class WorkflowAction(BaseModel):
    action_type: str  # e.g., SET_STATUS, CREATE_TASK, REQUIRE_APPROVAL, EMIT_EVENT
    parameters: Dict[str, Any] = Field(default_factory=dict)

class WorkflowCondition(BaseModel):
    condition_type: str # e.g., FIELD_EQUALS, APPROVAL_GRANTED, TASK_COMPLETED
    parameters: Dict[str, Any] = Field(default_factory=dict)

class WorkflowTransition(BaseModel):
    id: str = Field(default_factory=lambda: f"trans-{uuid.uuid4().hex[:8]}")
    from_state: str
    to_state: str
    label: Optional[str] = None
    conditions: List[WorkflowCondition] = Field(default_factory=list)

class WorkflowState(BaseModel):
    id: str
    label: str
    node_type: str = "TASK" # START, TASK, DECISION, APPROVAL, END
    entry_actions: List[WorkflowAction] = Field(default_factory=list)
    exit_actions: List[WorkflowAction] = Field(default_factory=list)
    ui_metadata: Dict[str, Any] = Field(default_factory=dict) # X/Y coordinates for designer

class WorkflowDefinitionMeta(BaseModel):
    id: Optional[str] = None
    name: str
    version: int = 1
    description: Optional[str] = None
    states: List[WorkflowState] = Field(default_factory=list)
    transitions: List[WorkflowTransition] = Field(default_factory=list)
    status: str = "DRAFT" # DRAFT | PUBLISHED | ARCHIVED


# ─────────────────────────────────────────────
# Runtime Models
# ─────────────────────────────────────────────

class WorkflowInstanceModel(BaseModel):
    id: str
    workflow_id: str
    target_entity_id: Optional[str] = None
    target_entity_type: Optional[str] = None
    status: str # RUNNING | COMPLETED | FAILED | CANCELLED
    current_state: str
    context_data: Dict[str, Any] = Field(default_factory=dict)
    started_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None

class WorkflowTaskModel(BaseModel):
    id: str
    instance_id: str
    title: str
    description: Optional[str] = None
    status: str # PENDING | IN_PROGRESS | COMPLETED | CANCELLED
    owner_id: Optional[str] = None
    department_id: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "MEDIUM"

class WorkflowApprovalModel(BaseModel):
    id: str
    instance_id: str
    task_id: Optional[str] = None
    status: str # PENDING | APPROVED | REJECTED
    approver_id: Optional[str] = None
    approver_department: Optional[str] = None
    comments: Optional[str] = None


# ─────────────────────────────────────────────
# Event Engine
# ─────────────────────────────────────────────

class WorkflowEvent(BaseModel):
    event_type: str
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=_now)
