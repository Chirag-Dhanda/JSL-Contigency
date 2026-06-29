"""
Domain models for Enterprise Integration Platform (EP-10).
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Connector Definitions ──────────────────────────────────────

class ConnectorStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


class ConnectorDefinition(BaseModel):
    connector_id: str = Field(default_factory=lambda: f"conn-{uuid.uuid4().hex[:8]}")
    name: str
    provider: str            # e.g., "SAP", "REST", "SQL"
    version: str = "1.0.0"
    status: ConnectorStatus = ConnectorStatus.DRAFT
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list) # READ, WRITE, DISCOVER
    created_at: datetime = Field(default_factory=_now)


# ── Transformation & Mapping ───────────────────────────────────

class FieldMapping(BaseModel):
    source_field: str
    target_field: str
    transform_rule: Optional[str] = None  # e.g., 'UPPER', 'ISO_DATE', 'TO_STRING'


class MappingRule(BaseModel):
    mapping_id: str = Field(default_factory=lambda: f"map-{uuid.uuid4().hex[:8]}")
    connector_id: str
    source_entity: str       # e.g., "EQUI" (SAP Equipment)
    target_entity: str       # EKOS Object Definition ID
    fields: List[FieldMapping] = Field(default_factory=list)
    version: int = 1


# ── Synchronization & Data Payloads ────────────────────────────

class SyncMode(str, Enum):
    INITIAL_LOAD = "INITIAL_LOAD"
    DELTA = "DELTA"
    MANUAL = "MANUAL"


class DataPayload(BaseModel):
    """Standardized representation of data entering or leaving EKOS."""
    external_id: str
    entity_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SyncSchedule(BaseModel):
    schedule_id: str = Field(default_factory=lambda: f"sched-{uuid.uuid4().hex[:8]}")
    connector_id: str
    mode: SyncMode = SyncMode.DELTA
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    is_active: bool = False
    last_run: Optional[datetime] = None


# ── Conflict Resolution ────────────────────────────────────────

class ConflictType(str, Enum):
    DUPLICATE = "DUPLICATE"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    VERSION_CONFLICT = "VERSION_CONFLICT"
    TRANSFORM_FAILURE = "TRANSFORM_FAILURE"


class ConflictRecord(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"conf-{uuid.uuid4().hex[:8]}")
    connector_id: str
    conflict_type: ConflictType
    external_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    error_message: str
    resolved: bool = False
    created_at: datetime = Field(default_factory=_now)


# ── Monitoring & Events ────────────────────────────────────────

class IntegrationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:8]}")
    connector_id: str
    action: str              # READ, WRITE, DISCOVER, SYNC
    status: str              # SUCCESS, FAILED
    records_processed: int = 0
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=_now)


# ── Governance Review ──────────────────────────────────────────

class IntegrationReviewPackage(BaseModel):
    """Human-in-the-loop review package required to activate connectors or enable writes."""
    package_id: str = Field(default_factory=lambda: f"irp-{uuid.uuid4().hex[:8]}")
    connector_id: str
    proposed_by: str
    action_requested: str    # e.g., "ACTIVATE_CONNECTOR", "ENABLE_WRITE"
    impact_analysis: str
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    reviewed_at: Optional[datetime] = None
