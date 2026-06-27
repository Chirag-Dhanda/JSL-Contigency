from typing import Optional, List, Any
from pydantic import BaseModel, Field

class FieldValidation(BaseModel):
    """Validation constraints defined visually by the Master Editor."""
    required: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    regex_pattern: Optional[str] = None
    allowed_values: Optional[List[str]] = None

class ObjectFieldDefinition(BaseModel):
    """
    A single field configured within the Object Designer.
    Maps to the UI Field Editor.
    """
    field_id: str = Field(..., description="Machine-readable key (e.g., 'voltage', 'ip_address')")
    display_name: str = Field(..., description="Human-readable label")
    field_type: str = Field(..., description="TEXT, NUMBER, BOOLEAN, DROPDOWN, MULTI_SELECT, DATE, FILE, ENTITY_REF")
    description: Optional[str] = None
    
    # UI Layout
    display_order: int = Field(default=0)
    grouping_tab: str = Field(default="General")
    
    # Logic
    default_value: Optional[Any] = None
    validation: FieldValidation = Field(default_factory=FieldValidation)
