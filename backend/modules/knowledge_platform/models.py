"""
modules/knowledge_platform/models.py
────────────────────────────────────────────────────────────────
EP-05: Domain models for the Knowledge Ingestion Platform.

These are the canonical Pydantic models used throughout the
knowledge_platform module. They are intentionally generic —
no manufacturing-specific types are embedded.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class AssetStatus(str, Enum):
    DRAFT = "DRAFT"
    INGESTING = "INGESTING"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class IngestionStatus(str, Enum):
    QUEUED = "QUEUED"
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    CHUNKING = "CHUNKING"
    EXTRACTING = "EXTRACTING"
    ONTOLOGY_MAPPING = "ONTOLOGY_MAPPING"
    RELATIONSHIP_DISCOVERY = "RELATIONSHIP_DISCOVERY"
    EMBEDDING = "EMBEDDING"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class CandidateStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ChunkStrategy(str, Enum):
    FIXED = "fixed"
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


# ─────────────────────────────────────────────
# Knowledge Asset
# ─────────────────────────────────────────────

class KnowledgeAsset(BaseModel):
    id: str = Field(default_factory=lambda: f"ka-{uuid.uuid4().hex[:12]}")
    title: str
    asset_type: str                       # SOP, POLICY, MANUAL, PROCEDURE, REFERENCE, etc.
    source_filename: Optional[str] = None
    source_uri: Optional[str] = None
    status: AssetStatus = AssetStatus.DRAFT
    version: int = 1
    language: str = "en"
    entity_type_ref: Optional[str] = None
    department_owner: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    published_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    extracted_metadata: Dict[str, Any] = Field(default_factory=dict)
    ontology_tags: List[str] = Field(default_factory=list)
    acl: Dict[str, Any] = Field(default_factory=dict)  # {roles: [], departments: []}


class KnowledgeAssetSummary(BaseModel):
    """Lightweight list view of a knowledge asset."""
    id: str
    title: str
    asset_type: str
    status: AssetStatus
    version: int
    department_owner: Optional[str]
    created_by: str
    created_at: datetime


# ─────────────────────────────────────────────
# Knowledge Chunk
# ─────────────────────────────────────────────

class KnowledgeChunk(BaseModel):
    id: str = Field(default_factory=lambda: f"kc-{uuid.uuid4().hex[:12]}")
    asset_id: str
    chunk_index: int
    chunk_strategy: ChunkStrategy = ChunkStrategy.FIXED
    text: str
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    token_count: Optional[int] = None
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    embedding_version: int = 1
    created_at: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Ingestion Job
# ─────────────────────────────────────────────

class StageLogEntry(BaseModel):
    stage: str
    status: str
    message: str
    timestamp: datetime = Field(default_factory=_now)

class IngestionJob(BaseModel):
    id: str = Field(default_factory=lambda: f"job-{uuid.uuid4().hex[:12]}")
    asset_id: Optional[str] = None
    filename: str
    file_type: str
    file_size_bytes: Optional[int] = None
    status: IngestionStatus = IngestionStatus.QUEUED
    current_stage: Optional[str] = None
    progress_pct: int = 0
    submitted_by: str
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    stage_log: List[StageLogEntry] = Field(default_factory=list)


# ─────────────────────────────────────────────
# Ontology & Relationship Candidates
# ─────────────────────────────────────────────

class OntologyCandidate(BaseModel):
    id: str = Field(default_factory=lambda: f"oc-{uuid.uuid4().hex[:12]}")
    asset_id: str
    concept_id: str
    concept_label: str
    confidence: float = 0.0
    source_text_snippet: Optional[str] = None
    status: CandidateStatus = CandidateStatus.PENDING
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

class RelationshipCandidate(BaseModel):
    id: str = Field(default_factory=lambda: f"rc-{uuid.uuid4().hex[:12]}")
    asset_id: str
    source_entity_id: str
    target_entity_id: Optional[str] = None
    target_entity_hint: Optional[str] = None
    relationship_type: str
    confidence: float = 0.0
    status: CandidateStatus = CandidateStatus.PENDING
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None


# ─────────────────────────────────────────────
# Review Package
# ─────────────────────────────────────────────

class KnowledgeReviewPackage(BaseModel):
    """Master Editor review package for a knowledge asset."""
    asset_id: str
    asset_title: str
    asset_status: AssetStatus
    extracted_metadata: Dict[str, Any]
    ontology_candidates: List[OntologyCandidate]
    relationship_candidates: List[RelationshipCandidate]
    chunk_count: int
    embedded_chunk_count: int
    embedding_coverage_pct: float
    quality_score: float
    duplicate_warnings: List[str]
    conflicts: List[str]
    recommendation: str   # "APPROVE" | "REVIEW_REQUIRED" | "REJECT"


# ─────────────────────────────────────────────
# RAG Context Package
# ─────────────────────────────────────────────

class RankedPassage(BaseModel):
    id: str
    asset_id: str
    asset_title: str
    asset_type: str
    chunk_index: int
    text: str
    score: float
    lexical_score: float = 0.0
    vector_score: float = 0.0
    graph_score: float = 0.0
    source_filename: Optional[str] = None
    version: int = 1

class ContextPackage(BaseModel):
    """The assembled retrieval context ready for a future LLM layer."""
    query: str
    passages: List[RankedPassage]
    total_found: int
    retrieval_strategy: str = "hybrid"  # lexical|vector|hybrid|graph
    permission_filtered: bool = True
    cited_sources: List[str] = Field(default_factory=list)
