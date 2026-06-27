from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid

class LifecycleState(str, Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    AI_REVIEWED = "AI_REVIEWED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"

class AuditRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"aud-{uuid.uuid4().hex[:8]}")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    user_id: str
    entity_id: str
    module: str
    action: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None

class VersionRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"ver-{uuid.uuid4().hex[:8]}")
    entity_id: str
    major_version: int
    minor_version: int
    patch_version: int
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    author_id: str
    snapshot: Dict[str, Any]
    version_notes: str
    ai_summary: Optional[str] = None

class ApprovalChain(BaseModel):
    id: str = Field(default_factory=lambda: f"chn-{uuid.uuid4().hex[:8]}")
    entity_id: str
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    steps: List[Dict[str, Any]] = Field(default_factory=list) # e.g. {"role": "MANAGER", "status": "APPROVED", "by": "u-123"}
