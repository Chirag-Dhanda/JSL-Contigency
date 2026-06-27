from pydantic import BaseModel, Field
from typing import List, Optional

class SOPAIResponse(BaseModel):
    """The strictly typed response model for the SOP Expert."""
    answer: str = Field(description="The generated AI response")
    referenced_sop: str = Field(description="The primary SOP being discussed")
    referenced_section: Optional[str] = Field(default=None, description="The specific section of the SOP")
    
    # Required Safety & Links
    mandatory_safety_notices: List[str] = Field(default_factory=list, description="Safety warnings injected by Validator")
    required_ppe: List[str] = Field(default_factory=list, description="PPE injected by Validator")
    
    related_equipment: List[str] = Field(default_factory=list, description="Equipment IDs")
    related_lessons: List[str] = Field(default_factory=list, description="Learning Module IDs")
    recommended_next_action: Optional[str] = Field(default=None, description="Suggested next procedural step")
    
    confidence: float = Field(ge=0.0, le=1.0, description="Overall confidence of the answer")
