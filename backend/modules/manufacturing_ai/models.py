from pydantic import BaseModel, Field
from typing import List, Optional

class KnowledgeSource(BaseModel):
    document_id: str
    title: str
    snippet: str
    relevance_score: float

class ManufacturingAIResponse(BaseModel):
    """The strictly typed response model for all Manufacturing Experts."""
    answer: str = Field(description="The generated AI response")
    knowledge_sources: List[KnowledgeSource] = Field(default_factory=list, description="RAG sources used")
    related_sops: List[str] = Field(default_factory=list, description="IDs of related SOPs")
    related_lessons: List[str] = Field(default_factory=list, description="IDs of related learning modules")
    related_equipment: List[str] = Field(default_factory=list, description="Equipment mentioned")
    recommended_next_learning: Optional[str] = Field(default=None, description="Suggested next step")
    confidence: float = Field(ge=0.0, le=1.0, description="Overall confidence of the answer")
    expert_used: str = Field(description="Which expert agent generated this response")
