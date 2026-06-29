"""
Domain models for Enterprise Event-Driven Platform (EP-11).
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)

# ── Core Events ──────────────────────────────────────────────────

class DomainEvent(BaseModel):
    """Base model for all events broadcast across the enterprise bus."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    version: int = 1
    timestamp: datetime = Field(default_factory=_now)
    source_module: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    classification: str = "INTERNAL"  # Ties into EP-09 Governance

    @classmethod
    def create(cls, event_type: str, source: str, payload: Dict[str, Any], correlation_id: Optional[str] = None, version: int = 1):
        return cls(
            event_type=event_type,
            version=version,
            source_module=source,
            payload=payload,
            correlation_id=correlation_id
        )

class EventSchema(BaseModel):
    event_type: str
    version: int
    schema_definition: Dict[str, Any] # JSON Schema mock
    description: str
    deprecated: bool = False

# ── Subscriptions & Processing ───────────────────────────────────

class SubscriptionRule(BaseModel):
    subscription_id: str = Field(default_factory=lambda: f"sub-{uuid.uuid4().hex[:8]}")
    event_type: str
    subscriber_name: str
    endpoint_or_handler: str
    is_active: bool = True
    max_retries: int = 3
    retry_backoff_ms: int = 1000
    filter_conditions: Dict[str, Any] = Field(default_factory=dict)

# ── Dead Letter Queue (DLQ) ──────────────────────────────────────

class DLQRecord(BaseModel):
    dlq_id: str = Field(default_factory=lambda: f"dlq-{uuid.uuid4().hex[:8]}")
    event: DomainEvent
    subscriber_name: str
    error_message: str
    stack_trace: Optional[str] = None
    retry_count: int
    last_attempt: datetime = Field(default_factory=_now)
    status: str = "FAILED" # FAILED, RETRYING, DISCARDED, RESOLVED

# ── Automation Engine ────────────────────────────────────────────

class AutomationActionType(str, Enum):
    TRIGGER_WORKFLOW = "TRIGGER_WORKFLOW"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"
    UPDATE_KNOWLEDGE = "UPDATE_KNOWLEDGE"
    HTTP_WEBHOOK = "HTTP_WEBHOOK"

class AutomationRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: f"auto-{uuid.uuid4().hex[:8]}")
    name: str
    trigger_event_type: str
    conditions: Dict[str, Any] = Field(default_factory=dict)
    action_type: AutomationActionType
    action_payload_template: Dict[str, Any]
    is_active: bool = False
    requires_approval: bool = True # Security constraint from EP-09

class AutomationReviewPackage(BaseModel):
    package_id: str = Field(default_factory=lambda: f"arp-{uuid.uuid4().hex[:8]}")
    rule_id: str
    proposed_by: str
    status: str = "PENDING"
    impact_analysis: str
    created_at: datetime = Field(default_factory=_now)
