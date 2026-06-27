import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from .lifecycle import EntityLifecycle

class EnterpriseEntity(BaseModel):
    """
    The generalized foundation for ALL business objects in the enterprise.
    Replacing fixed SQL tables with a dynamic, metadata-driven architecture.
    """
    # Core Identity
    id: str = Field(default_factory=lambda: f"ent-{uuid.uuid4().hex[:12]}")
    name: str = Field(..., description="System name of the entity")
    entity_type: str = Field(..., description="The registered Type ID (e.g., 'plc_device', 'sop')")
    display_name: str = Field(..., description="Human readable name")
    description: Optional[str] = None
    
    # Hierarchy & Graph
    parent_entity_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    # Lifecycle & Versioning
    status: EntityLifecycle = Field(default=EntityLifecycle.DRAFT)
    version: int = Field(default=1)
    
    # Audit
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Access Control
    permission_profile: str = Field(default="default_entity_profile")
    
    # The Core Engine (Dynamic Data)
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="The dynamic JSON payload holding all custom properties for this specific entity type."
    )
    
    # System Indexes
    ai_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Data specifically formatted or generated for the AI Orchestrator (e.g., summaries, embeddings)."
    )
    search_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flattened strings optimized for global Elastic/Lexical search."
    )
