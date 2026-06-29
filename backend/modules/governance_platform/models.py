"""
Domain models for Enterprise Governance, Security & Zero-Trust Access Platform (EP-09).
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# Classification Framework
# ─────────────────────────────────────────────

class ClassificationLevel(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"
    HIGHLY_CONFIDENTIAL = "HIGHLY_CONFIDENTIAL"
    SAFETY_CRITICAL = "SAFETY_CRITICAL"
    EXPORT_CONTROLLED = "EXPORT_CONTROLLED"


CLASSIFICATION_RANK: Dict[ClassificationLevel, int] = {
    ClassificationLevel.PUBLIC: 0,
    ClassificationLevel.INTERNAL: 1,
    ClassificationLevel.RESTRICTED: 2,
    ClassificationLevel.CONFIDENTIAL: 3,
    ClassificationLevel.HIGHLY_CONFIDENTIAL: 4,
    ClassificationLevel.SAFETY_CRITICAL: 5,
    ClassificationLevel.EXPORT_CONTROLLED: 6,
}


class ClassificationTag(BaseModel):
    asset_id: str
    asset_type: str
    level: ClassificationLevel
    reason: Optional[str] = None
    tagged_by: str
    tagged_at: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Policy Engine
# ─────────────────────────────────────────────

class PolicyType(str, Enum):
    ACCESS = "ACCESS"
    RETENTION = "RETENTION"
    KNOWLEDGE = "KNOWLEDGE"
    WORKFLOW = "WORKFLOW"
    AI = "AI"
    SEARCH = "SEARCH"
    CLASSIFICATION = "CLASSIFICATION"
    COMPLIANCE = "COMPLIANCE"


class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class EnterprisePolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"pol-{uuid.uuid4().hex[:8]}")
    name: str
    version: int = 1
    policy_type: PolicyType
    status: PolicyStatus = PolicyStatus.DRAFT
    description: Optional[str] = None
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    applies_to_roles: List[str] = Field(default_factory=list)    # Empty = all roles
    applies_to_depts: List[str] = Field(default_factory=list)    # Empty = all departments
    created_by: str = "SYSTEM"
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


class PolicyDecision(BaseModel):
    granted: bool
    policy_id: Optional[str] = None
    reason: str = ""
    conditions: List[str] = Field(default_factory=list)   # Any conditional access restrictions


# ─────────────────────────────────────────────
# Field-Level Security
# ─────────────────────────────────────────────

class FieldVisibility(str, Enum):
    VISIBLE = "VISIBLE"
    READ_ONLY = "READ_ONLY"
    MASKED = "MASKED"           # e.g. show last 4 chars only
    HIDDEN = "HIDDEN"
    DEPT_RESTRICTED = "DEPT_RESTRICTED"


class FieldPermission(BaseModel):
    object_type: str
    field_name: str
    visibility: FieldVisibility
    required_roles: List[str] = Field(default_factory=list)
    required_depts: List[str] = Field(default_factory=list)
    classification: ClassificationLevel = ClassificationLevel.INTERNAL


# ─────────────────────────────────────────────
# Row-Level Security
# ─────────────────────────────────────────────

class RLSContext(BaseModel):
    user_id: str
    roles: List[str] = Field(default_factory=list)
    department_id: Optional[str] = None
    max_classification: ClassificationLevel = ClassificationLevel.INTERNAL


class RLSFilter(BaseModel):
    """Represents a predicate to be injected into a SQLAlchemy query."""
    filter_type: str      # OWNED_BY | DEPT_MATCH | CLASSIFICATION_MAX | WORKFLOW_STATE
    column: str
    operator: str         # eq | lte | in | is_null
    value: Any


# ─────────────────────────────────────────────
# Security Monitoring
# ─────────────────────────────────────────────

class SecurityEventType(str, Enum):
    AUTH_SUCCESS = "AUTH_SUCCESS"
    AUTH_FAILURE = "AUTH_FAILURE"
    AUTHZ_DENIED = "AUTHZ_DENIED"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    REPEATED_FAILURE = "REPEATED_FAILURE"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    AI_PERMISSION_BLOCK = "AI_PERMISSION_BLOCK"
    SEARCH_FILTER_APPLIED = "SEARCH_FILTER_APPLIED"
    CLASSIFICATION_BREACH_ATTEMPT = "CLASSIFICATION_BREACH_ATTEMPT"
    GOVERNANCE_CHANGE = "GOVERNANCE_CHANGE"
    SESSION_EXPIRED = "SESSION_EXPIRED"


class SecurityEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"sec-{uuid.uuid4().hex[:8]}")
    event_type: SecurityEventType
    severity: str = "INFO"          # INFO | WARN | CRITICAL
    actor_id: Optional[str] = None
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Governance & Human-in-the-Loop
# ─────────────────────────────────────────────

class GovernanceChangeType(str, Enum):
    POLICY_CHANGE = "POLICY_CHANGE"
    ROLE_CHANGE = "ROLE_CHANGE"
    CLASSIFICATION_CHANGE = "CLASSIFICATION_CHANGE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    DEPT_HIERARCHY_CHANGE = "DEPT_HIERARCHY_CHANGE"
    GOVERNANCE_RULE_CHANGE = "GOVERNANCE_RULE_CHANGE"
    KNOWLEDGE_GOVERNANCE = "KNOWLEDGE_GOVERNANCE"
    WORKFLOW_GOVERNANCE = "WORKFLOW_GOVERNANCE"


class GovernanceReviewStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class GovernanceReviewPackage(BaseModel):
    package_id: str = Field(default_factory=lambda: f"gov-{uuid.uuid4().hex[:8]}")
    change_type: GovernanceChangeType
    proposed_by: str
    description: str
    current_state: Optional[Dict[str, Any]] = None
    proposed_state: Dict[str, Any] = Field(default_factory=dict)
    impact_analysis: str = ""
    status: GovernanceReviewStatus = GovernanceReviewStatus.PENDING
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    reviewed_at: Optional[datetime] = None


# ─────────────────────────────────────────────
# Compliance
# ─────────────────────────────────────────────

class ComplianceStandard(str, Enum):
    ISO_9001 = "ISO_9001"
    ISO_27001 = "ISO_27001"
    SOC_2 = "SOC_2"
    GDPR = "GDPR"
    IEC_62443 = "IEC_62443"    # Industrial cybersecurity
    INTERNAL = "INTERNAL"


class ComplianceRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"comp-{uuid.uuid4().hex[:8]}")
    standard: ComplianceStandard
    control_id: str
    control_name: str
    status: str = "PENDING"    # PENDING | COMPLIANT | NON_COMPLIANT | NOT_APPLICABLE
    evidence_ids: List[str] = Field(default_factory=list)
    last_reviewed: Optional[datetime] = None
    notes: Optional[str] = None
