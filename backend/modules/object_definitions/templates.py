import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from .fields import ObjectFieldDefinition
from .behavior import ObjectBehavior, AIObjectRules

class VisualObjectDefinition(BaseModel):
    """
    The master blueprint created in the Object Designer UI.
    This is what the RuntimeGenerator compiles into an EntityTypeDefinition.
    """
    id: str = Field(default_factory=lambda: f"obj-{uuid.uuid4().hex[:8]}")
    type_id: str = Field(..., description="The registry ID (e.g., 'equipment', 'sop')")
    display_name: str = Field(..., description="Human readable name")
    description: Optional[str] = None
    icon: str = Field(default="box")
    
    fields: List[ObjectFieldDefinition] = Field(default_factory=list)
    behavior: ObjectBehavior
    
    # State in the designer
    status: str = Field(default="DRAFT", description="DRAFT or ACTIVE (compiled)")

# --- Standard Templates ---

def get_equipment_template() -> VisualObjectDefinition:
    return VisualObjectDefinition(
        type_id="equipment",
        display_name="Equipment",
        description="Physical machinery on the factory floor.",
        icon="server",
        behavior=ObjectBehavior(
            ai_rules=AIObjectRules(
                description="This represents physical machinery. Crucial for LOTO and maintenance queries.",
                ai_tags=["machine", "asset", "hardware"],
                search_priority=80
            )
        )
    )

def get_sop_template() -> VisualObjectDefinition:
    return VisualObjectDefinition(
        type_id="sop",
        display_name="Standard Operating Procedure",
        description="Official instructional documents.",
        icon="book-open",
        behavior=ObjectBehavior(
            ai_rules=AIObjectRules(
                description="Official procedural document. The AI must prioritize this for 'how-to' questions.",
                ai_tags=["procedure", "instruction", "document"],
                search_priority=100
            )
        )
    )
