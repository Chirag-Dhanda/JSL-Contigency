from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StageConfiguration(BaseModel):
    """Configuration for a single manufacturing stage."""
    estimated_duration_minutes: int = 0
    required_sops: List[str] = Field(default_factory=list)
    required_lessons: List[str] = Field(default_factory=list)
    required_ppe: List[str] = Field(default_factory=list)
    quality_checks: List[str] = Field(default_factory=list)
    
class ProcessNode(BaseModel):
    """Represents a node in the visual flow builder."""
    id: str
    type: str = Field(..., description="E.g., 'manufacturing_stage', 'quality_gate', 'department'")
    label: str
    department_id: Optional[str] = None
    equipment_ids: List[str] = Field(default_factory=list)
    configuration: StageConfiguration = Field(default_factory=StageConfiguration)
    
    # Visual positioning
    position_x: float = 0.0
    position_y: float = 0.0

class ProcessEdge(BaseModel):
    """Represents a directional connection between nodes."""
    id: str
    source_id: str
    target_id: str
    label: Optional[str] = None
    edge_type: str = Field(default="NEXT_STAGE") # e.g., NEXT_STAGE, REWORK, ESCALATION

class ManufacturingFlow(BaseModel):
    """The master document exported by the Visual Flow Builder."""
    id: str = Field(..., description="Unique flow ID")
    name: str
    plant_id: str
    nodes: List[ProcessNode] = Field(default_factory=list)
    edges: List[ProcessEdge] = Field(default_factory=list)
    is_published: bool = False
