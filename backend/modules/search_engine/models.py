"""
Domain models for Enterprise Search & Context Engine (EP-06).
"""
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)

# ─────────────────────────────────────────────
# Inputs & Planning
# ─────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    user_department: Optional[str] = None
    user_roles: List[str] = Field(default_factory=list)
    
    # Metadata filters
    asset_types: List[str] = Field(default_factory=list)
    ontology_tags: List[str] = Field(default_factory=list)
    
    # Depth/Tuning
    max_results: int = 10
    include_graph_expansion: bool = True
    min_confidence_score: float = 0.0

class RetrievalStrategy(BaseModel):
    name: str
    enabled: bool = True
    weight: float = 1.0

class RetrievalPlan(BaseModel):
    """Output of the Query Planner."""
    plan_id: str = Field(default_factory=lambda: f"plan-{uuid.uuid4().hex[:8]}")
    original_query: str
    optimized_query: str
    strategies: List[RetrievalStrategy] = Field(default_factory=list)
    target_asset_types: List[str] = Field(default_factory=list)
    required_departments: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# Search Results & Ranking
# ─────────────────────────────────────────────

class RankedPassage(BaseModel):
    id: str
    asset_id: str
    asset_title: str
    asset_type: str
    chunk_index: int
    text: str
    
    # Scores
    final_score: float = 0.0
    lexical_score: float = 0.0
    vector_score: float = 0.0
    graph_score: float = 0.0
    ontology_score: float = 0.0
    
    # Provenance
    source_filename: Optional[str] = None
    version: int = 1


# ─────────────────────────────────────────────
# Citations & Context
# ─────────────────────────────────────────────

class Citation(BaseModel):
    citation_id: str = Field(default_factory=lambda: f"cite-{uuid.uuid4().hex[:8]}")
    asset_id: str
    asset_title: str
    chunk_id: str
    relevance_score: float
    timestamp: datetime = Field(default_factory=_now)

class ContextPackage(BaseModel):
    """The final output consumed by LLMs."""
    package_id: str = Field(default_factory=lambda: f"ctx-{uuid.uuid4().hex[:12]}")
    original_query: str
    passages: List[RankedPassage] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    total_tokens_estimated: int = 0
    permission_filtered: bool = True
    generated_at: datetime = Field(default_factory=_now)


# ─────────────────────────────────────────────
# Search Session & History
# ─────────────────────────────────────────────

class SearchSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"sess-{uuid.uuid4().hex[:12]}")
    user_id: str
    queries: List[str] = Field(default_factory=list)
    last_context_package_id: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

class SearchRecommendation(BaseModel):
    query: str
    reason: str # e.g., "Related to your department", "Popular among operators"
