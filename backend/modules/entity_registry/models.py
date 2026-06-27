from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ValidationRule(BaseModel):
    """Defines a validation constraint for a dynamic metadata field."""
    field_type: str = Field(..., description="e.g., 'text', 'long_text', 'rich_text', 'number', 'decimal', 'currency', 'percentage', 'boolean', 'date', 'datetime', 'duration', 'email', 'phone', 'url', 'dropdown', 'multi_select', 'reference', 'file', 'image', 'video', 'document', 'ai_generated', 'calculated', 'sap_placeholder'")
    required: bool = Field(default=False)
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enum_values: Optional[List[str]] = None
    regex: Optional[str] = None
    unique: bool = Field(default=False)
    default_value: Optional[Any] = None
    visibility_rule: Optional[str] = None
    role_restrictions: Optional[List[str]] = None
    conditional_requirement: Optional[str] = None

class EntityTypeDefinition(BaseModel):
    """
    Defines the schema for a dynamic entity type.
    Example: 'plc_device', 'department', 'sop'
    """
    type_id: str = Field(..., description="Unique internal identifier (e.g., 'plc_device')")
    display_name: str = Field(..., description="Human readable name (e.g., 'PLC Device')")
    description: Optional[str] = None
    icon: Optional[str] = Field(default="fa-cube")
    category: Optional[str] = Field(default="General")
    version: int = Field(default=1)
    status: str = Field(default="Draft", description="Draft, Review, Published, Archived")
    ownership: Optional[str] = Field(default="system")
    visibility: str = Field(default="public", description="public, private, restricted")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Custom configurations for the type")
    
    # The Schema Rules
    metadata_schema: Dict[str, ValidationRule] = Field(
        default_factory=dict,
        description="Maps a metadata key (e.g., 'commission_date') to its ValidationRule."
    )
    
    # Default values for new entities of this type
    default_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Configuration
    is_active: bool = Field(default=True)
    allow_custom_fields: bool = Field(
        default=True, 
        description="If true, entities can have metadata fields not explicitly defined in the schema."
    )
