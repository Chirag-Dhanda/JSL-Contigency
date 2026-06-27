from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import ResourceType

class ResourceMetadata(BaseModel):
    author_id: str
    version: str
    difficulty_level: Optional[str] = None
    tags: List[str] = []
    category: str
    subcategory: Optional[str] = None
    created_at: datetime
    last_updated: datetime

class ResourceRelationship(BaseModel):
    learning_module_ids: List[str] = []
    lesson_ids: List[str] = []
    sop_ids: List[str] = []
    equipment_ids: List[str] = []
    manufacturing_stage_ids: List[str] = []
    assessment_ids: List[str] = []
    certificate_ids: List[str] = []
    safety_module_ids: List[str] = []
    
    # Future SAP
    sap_document_ids: List[str] = []

class ResourceAsset(BaseModel):
    id: str
    title: str
    description: str
    resource_type: ResourceType
    file_url: str
    department_id: Optional[str] = None
    
    metadata: ResourceMetadata
    relationships: ResourceRelationship

class UserResourceInteraction(BaseModel):
    user_id: str
    bookmarked_resource_ids: List[str] = []
    favorite_resource_ids: List[str] = []
    recently_viewed_ids: List[str] = []
    pinned_resource_ids: List[str] = []
