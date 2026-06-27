from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentMetadata(BaseModel):
    department: str = Field(..., description="The department owning this knowledge.")
    role_access: List[str] = Field(..., description="Roles permitted to access this.")
    knowledge_type: str = Field(..., description="Type (e.g., manual, guideline, log).")
    author: str
    version: str
    security_level: int = Field(default=1, description="1=Public, 5=Top Secret")
    language: str = Field(default="en")
    tags: List[str] = []
    document_source: str = Field(..., description="URL or internal ID of original source")
    creation_date: datetime
    approval_status: Optional[str] = None
