from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class PromptStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class PromptTemplate(BaseModel):
    """The enterprise structure for an AI prompt."""
    prompt_id: str
    name: str
    category: str = Field(description="e.g., Manufacturing, Safety, SOP")
    description: str
    
    # Prompt Content
    system_prompt: str
    prompt_body: str
    variables: List[str] = Field(default_factory=list, description="Variables expected e.g., {user_id}")
    default_values: Dict[str, str] = Field(default_factory=dict)
    
    # Lifecycle Metadata
    version: str = Field(default="1.0.0")
    status: PromptStatus = Field(default=PromptStatus.DRAFT)
    author: str
    reviewer: Optional[str] = None
    approval_date: Optional[str] = None
