from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedEntity(BaseModel):
    """Represents a piece of knowledge extracted from a document."""
    entity_id: str
    entity_type: str = Field(description="e.g., Equipment, Role, Process, Concept")
    entity_value: str = Field(description="The actual extracted string")
    
    # Traceability & Confidence
    confidence_score: float = Field(ge=0.0, le=1.0, description="AI confidence in this extraction")
    extraction_source: str = Field(description="The chunk or text block this came from")
    document_reference_id: str = Field(description="Parent Document ID")
    page_number: Optional[int] = Field(default=None, description="Page number if applicable")
    section_name: Optional[str] = Field(default=None, description="Header or section name")
    
    # Future Graph properties
    properties: dict = Field(default_factory=dict, description="Additional context attributes")
