from typing import List, Optional
from pydantic import BaseModel, Field

class AIObjectRules(BaseModel):
    """Dictates how the AI Orchestrator interprets this object type."""
    description: str = Field(..., description="Prompt injected into the AI context explaining what this object is.")
    ai_tags: List[str] = Field(default_factory=list)
    search_priority: int = Field(default=50, description="0-100 score. Higher priority surfaces first in AI search.")
    summarization_rules: Optional[str] = Field(None, description="Custom prompt for summarizing instances of this object.")
    embedding_policy: str = Field(default="ALL_FIELDS", description="Which fields to vectorize: ALL_FIELDS, SELECTED_FIELDS, NONE")

class ObjectBehavior(BaseModel):
    """Configuration for how the platform treats this object."""
    publishing_workflow_enabled: bool = Field(default=True)
    versioning_enabled: bool = Field(default=True)
    searchable: bool = Field(default=True)
    navigation_visible: bool = Field(default=True)
    ai_rules: AIObjectRules
