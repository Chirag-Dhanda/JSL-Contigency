"""
Domain models for Enterprise AI Orchestration Platform (EP-08).
"""
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# LLM Provider I/O
# ─────────────────────────────────────────────

class LLMGenerationOptions(BaseModel):
    model: Optional[str] = None        # Provider-specific model override
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    stream: bool = False

class LLMResponse(BaseModel):
    provider: str
    model: str
    raw_text: str
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0


# ─────────────────────────────────────────────
# Prompt Templates
# ─────────────────────────────────────────────

class PromptTemplate(BaseModel):
    template_id: str = Field(default_factory=lambda: f"tmpl-{uuid.uuid4().hex[:8]}")
    name: str
    version: int = 1
    skill: str = "general"                     # Skill this template belongs to
    system_template: str
    user_template: str                         # May use {query}, {context}, {role}, {department}


class AssembledPrompt(BaseModel):
    template_id: str
    template_version: int
    system_prompt: str
    user_prompt: str
    estimated_tokens: int = 0


# ─────────────────────────────────────────────
# Chat & Conversation
# ─────────────────────────────────────────────

class AIChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None     # Resume existing conversation
    skill: str = "knowledge_qa"               # Which AI skill to invoke
    user_department: Optional[str] = None
    user_roles: List[str] = Field(default_factory=list)
    linked_entity_id: Optional[str] = None    # E.g. an equipment or SOP object
    linked_workflow_id: Optional[str] = None
    options: LLMGenerationOptions = Field(default_factory=LLMGenerationOptions)

class ConversationTurn(BaseModel):
    turn_id: str = Field(default_factory=lambda: f"turn-{uuid.uuid4().hex[:8]}")
    role: str                                 # "user" | "assistant"
    content: str
    skill: Optional[str] = None
    prompt_template_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    citation_ids: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=_now)

class Conversation(BaseModel):
    conversation_id: str = Field(default_factory=lambda: f"conv-{uuid.uuid4().hex[:12]}")
    user_id: str
    title: Optional[str] = None
    linked_entity_id: Optional[str] = None
    linked_workflow_id: Optional[str] = None
    turns: List[ConversationTurn] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

class AIChatResponse(BaseModel):
    conversation_id: str
    turn_id: str
    answer: str
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    skill: str
    provider: str
    model: str
    validation_passed: bool = True
    validation_notes: List[str] = Field(default_factory=list)
    tokens_used: int = 0
    latency_ms: float = 0.0
    generated_at: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Validation & Review
# ─────────────────────────────────────────────

class ValidationResult(BaseModel):
    passed: bool
    issues: List[str] = Field(default_factory=list)
    confidence_level: str = "HIGH"             # HIGH | MEDIUM | LOW | UNKNOWN

class AIReviewPackage(BaseModel):
    """Human-in-the-loop review package for AI-suggested enterprise changes."""
    package_id: str = Field(default_factory=lambda: f"air-{uuid.uuid4().hex[:8]}")
    original_query: str
    context_summary: str
    suggested_changes: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    validation: Optional[ValidationResult] = None
    prompt_template_id: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Observability
# ─────────────────────────────────────────────

class AIObservabilityRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"obs-{uuid.uuid4().hex[:8]}")
    conversation_id: Optional[str] = None
    turn_id: Optional[str] = None
    skill: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    context_passages: int = 0
    citations_injected: int = 0
    validation_passed: bool = True
    timestamp: datetime = Field(default_factory=_now)
