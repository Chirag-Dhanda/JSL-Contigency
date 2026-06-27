from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from .enums import ContentStatus, ApprovalRole

class ChangeLog(BaseModel):
    changed_by_user_id: str
    change_description: str
    timestamp: datetime

class VersionInfo(BaseModel):
    major: int = 1
    minor: int = 0
    patch: int = 0
    author_id: str
    approver_ids: List[str] = []
    created_at: datetime
    published_at: Optional[datetime] = None
    last_updated: datetime
    change_history: List[ChangeLog] = []

    @property
    def version_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

class ApprovalStep(BaseModel):
    role: ApprovalRole
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    approved_by_user_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    comments: Optional[str] = None

class ApprovalWorkflow(BaseModel):
    id: str
    name: str
    steps: List[ApprovalStep]

class ContentItem(BaseModel):
    id: str
    title: str
    description: str
    payload_ref_id: str # Reference to the actual raw data (e.g., Lesson body, file UUID)
    status: ContentStatus = ContentStatus.DRAFT
    version_info: VersionInfo
    active_workflow_id: Optional[str] = None
    active_workflow_state: List[ApprovalStep] = []
    ai_metadata_hooks: Dict[str, str] = {} # For Future AI Tagging/Processing
