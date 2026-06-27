from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .enums import ContentType, ContentStatus, DifficultyLevel, OrganizationType, RelationshipType

class KnowledgeRelationship(BaseModel):
    target_object_id: str
    relationship_type: RelationshipType

class KnowledgeObject(BaseModel):
    id: str
    title: str
    description: str
    content_type: ContentType
    
    # Metadata
    category: str
    department: Optional[str] = None
    role: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    tags: List[str] = []
    
    # Execution details
    estimated_time_mins: int = 15
    learning_objectives: List[str] = []
    prerequisites: List[str] = []
    relationships: List[KnowledgeRelationship] = []
    
    # Lifecycle & Versioning
    author: str
    author_id: str
    version: str = "1.0.0"
    status: ContentStatus = ContentStatus.DRAFT
    created_at: datetime
    updated_at: datetime
    
    # The actual payload or reference (URI)
    content_payload: Dict[str, str] = {}
    
    # Future
    ai_embeddings_indexed: bool = False

class ContentGroup(BaseModel):
    id: str
    title: str
    description: str
    organization_type: OrganizationType
    parent_id: Optional[str] = None
    object_ids: List[str] = []
