"""
Domain models for Enterprise Administration & Control Center (EP-13).
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

def _now() -> datetime:
    return datetime.now(timezone.utc)

# ── Configuration Platform ───────────────────────────────────────────────────

class ConfigurationSetting(BaseModel):
    key: str
    value: Any
    type: str  # "boolean", "string", "json", "integer"
    description: str
    requires_restart: bool = False
    is_sensitive: bool = False
    updated_at: datetime = Field(default_factory=_now)
    updated_by: str = "system"

class ConfigurationVersion(BaseModel):
    version_id: str = Field(default_factory=lambda: f"ver-{uuid.uuid4().hex[:8]}")
    timestamp: datetime = Field(default_factory=_now)
    created_by: str
    changes: Dict[str, Any]
    rollback_supported: bool = True

# ── Feature Management ───────────────────────────────────────────────────────

class FeatureFlag(BaseModel):
    key: str
    is_enabled: bool
    description: str
    environments: List[str] = Field(default_factory=lambda: ["production", "staging", "development"])
    allowed_roles: List[str] = Field(default_factory=lambda: ["*"])
    updated_at: datetime = Field(default_factory=_now)

# ── Review & Approval Center ─────────────────────────────────────────────────

class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ReviewQueueItem(BaseModel):
    """
    Unified wrapper for governance review packages consumed by the Admin UI.
    """
    queue_id: str = Field(default_factory=lambda: f"rev-{uuid.uuid4().hex[:8]}")
    governance_package_id: str
    action_type: str  # "METADATA_UPDATE", "RESTORE_BACKUP", "ACTIVATE_CONNECTOR", etc.
    requested_by: str
    impact_summary: str
    status: ReviewStatus = ReviewStatus.PENDING
    created_at: datetime = Field(default_factory=_now)
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None

# ── Environment & Tenant Management ──────────────────────────────────────────

class TenantEnvironment(BaseModel):
    environment_id: str
    name: str # e.g. "Production"
    tenant_id: str = "default"
    is_active: bool = True
    base_url: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
