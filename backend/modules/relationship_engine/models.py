import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from modules.entity_framework.lifecycle import EntityLifecycle

class EnterpriseRelationship(BaseModel):
    """
    Represents a directed or bidirectional edge between two EnterpriseEntities.
    """
    id: str = Field(default_factory=lambda: f"rel-{uuid.uuid4().hex[:12]}")
    
    # Connection Points
    source_entity_id: str = Field(..., description="The ID of the origin entity.")
    target_entity_id: str = Field(..., description="The ID of the destination entity.")
    relationship_type: str = Field(..., description="The registered Type ID (e.g., 'belongs_to')")
    
    # Graph Properties
    direction: str = Field(default="DIRECTED", description="'DIRECTED' or 'BIDIRECTIONAL'")
    weight: float = Field(default=1.0, description="Used for pathfinding/priority algorithms")
    priority: int = Field(default=0)
    
    # State
    status: EntityLifecycle = Field(default=EntityLifecycle.PUBLISHED)
    description: Optional[str] = None
    
    # Dynamic Data on the Edge
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom properties for this specific relationship instance."
    )
    
    # Audit
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = Field(default=1)
    
    # System Indexes
    permission_profile: str = Field(default="default_rel_profile")
    ai_metadata: Dict[str, Any] = Field(default_factory=dict)
