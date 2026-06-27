from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import SOPStatus, SOPCategory, WorkflowRole

class SOPSection(BaseModel):
    id: str
    title: str # e.g., PURPOSE, SCOPE, PROCEDURE
    content: str
    order_index: int

class SOPMetadata(BaseModel):
    sop_number: str
    revision_number: int
    version: str # e.g., 1.0.0
    author_id: str
    reviewer_ids: List[str] = []
    approver_ids: List[str] = []
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    created_at: datetime
    last_updated: datetime

class SOPWorkflowStep(BaseModel):
    role: WorkflowRole
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    approved_by_user_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    comments: Optional[str] = None

class SOPDocument(BaseModel):
    id: str
    title: str
    department_id: str
    category: SOPCategory
    status: SOPStatus
    metadata: SOPMetadata
    sections: List[SOPSection] = []
    
    active_workflow_state: List[SOPWorkflowStep] = []
    
    # Future AI Integration Hooks
    ai_summary_prompt: Optional[str] = None
    ai_question_prompt: Optional[str] = None
