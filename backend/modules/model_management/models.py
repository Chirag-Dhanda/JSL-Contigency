from pydantic import BaseModel, Field
from typing import List, Optional

class AIModelConfig(BaseModel):
    """Configuration for a specific AI model."""
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    top_k: int = Field(default=40, ge=1)
    max_tokens: int = Field(default=4096, ge=1)
    context_length: int = Field(default=8192, ge=1)
    timeout_ms: int = Field(default=30000)

class InstalledModel(BaseModel):
    """Represents a locally available LLM or Embedding Model."""
    model_id: str
    display_name: str
    capabilities: List[str] = Field(default_factory=list, description="e.g. ['chat', 'embeddings', 'vision']")
    is_enabled: bool = Field(default=True)
    is_default_chat: bool = Field(default=False)
    is_default_embedding: bool = Field(default=False)
    config: AIModelConfig = Field(default_factory=AIModelConfig)
