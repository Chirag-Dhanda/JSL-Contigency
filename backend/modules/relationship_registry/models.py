from typing import List, Optional
from pydantic import BaseModel, Field

class RelationshipTypeDefinition(BaseModel):
    """
    Defines the schema and rules for a type of connection between entities.
    Example: 'belongs_to', 'operates', 'requires'
    """
    type_id: str = Field(..., description="Unique identifier (e.g., 'belongs_to')")
    display_name: str = Field(..., description="Human readable name")
    description: Optional[str] = None
    
    # Constraints
    allowed_source_types: Optional[List[str]] = Field(
        default=None, 
        description="List of Entity Types allowed as the source. None means any."
    )
    allowed_target_types: Optional[List[str]] = Field(
        default=None, 
        description="List of Entity Types allowed as the target. None means any."
    )
    
    # Graph characteristics
    is_directed: bool = Field(default=True, description="True for A->B, False for A<->B")
    is_active: bool = Field(default=True)
