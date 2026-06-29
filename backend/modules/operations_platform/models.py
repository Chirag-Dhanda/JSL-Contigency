"""
Domain models for Enterprise Operations Platform (EP-12).
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Health Management ────────────────────────────────────────────────────────

class HealthStatus(str, Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

class ComponentHealth(BaseModel):
    component_name: str
    status: HealthStatus
    latency_ms: float = 0.0
    message: Optional[str] = None
    last_checked: datetime = Field(default_factory=_now)

class SystemHealth(BaseModel):
    overall_status: HealthStatus
    timestamp: datetime = Field(default_factory=_now)
    components: Dict[str, ComponentHealth] = Field(default_factory=dict)


# ── Telemetry (Traces & Metrics) ─────────────────────────────────────────────

class TraceSpan(BaseModel):
    trace_id: str
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tags: Dict[str, str] = Field(default_factory=dict)
    
    @property
    def duration_ms(self) -> Optional[float]:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return None

class MetricRecord(BaseModel):
    name: str
    value: float
    unit: str  # ms, count, bytes, percent
    timestamp: datetime = Field(default_factory=_now)
    tags: Dict[str, str] = Field(default_factory=dict)


# ── Alerts & Incidents ───────────────────────────────────────────────────────

class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class AlertRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: f"alt-{uuid.uuid4().hex[:8]}")
    metric_name: str
    condition: str  # e.g. ">", "<", "=="
    threshold: float
    severity: AlertSeverity
    is_active: bool = True

class IncidentRecord(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc-{uuid.uuid4().hex[:8]}")
    title: str
    severity: AlertSeverity
    status: str = "OPEN" # OPEN, INVESTIGATING, RESOLVED
    affected_components: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)
    resolved_at: Optional[datetime] = None
    root_cause: Optional[str] = None


# ── Capacity & Diagnostics ───────────────────────────────────────────────────

class CapacityForecast(BaseModel):
    resource_name: str
    current_usage: float
    projected_usage_30d: float
    unit: str
    timestamp: datetime = Field(default_factory=_now)


# ── Backup & Operations ──────────────────────────────────────────────────────

class BackupRecord(BaseModel):
    backup_id: str = Field(default_factory=lambda: f"bup-{uuid.uuid4().hex[:8]}")
    component: str  # DB, VECTOR, CONFIG
    status: str = "IN_PROGRESS" # SUCCESS, FAILED
    size_bytes: Optional[int] = None
    location_uri: Optional[str] = None
    started_at: datetime = Field(default_factory=_now)
    completed_at: Optional[datetime] = None

class OperationsReviewPackage(BaseModel):
    package_id: str = Field(default_factory=lambda: f"orp-{uuid.uuid4().hex[:8]}")
    operation_type: str # RESTORE, PURGE, REINDEX
    requested_by: str
    target_component: str
    impact_analysis: str
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=_now)
