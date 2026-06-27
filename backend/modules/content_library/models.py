from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import ContentType, CollectionType

class LibraryItem(BaseModel):
    id: str
    content_item_id: str # Link back to the versioned LCMS ContentItem
    title: str
    description: str
    content_type: ContentType
    
    # Search & Organization Metadata
    categories: List[str] = []
    departments: List[str] = []
    tags: List[str] = []
    manufacturing_stages: List[str] = []
    equipment_ids: List[str] = []
    role_ids: List[str] = []
    
    published_version: str
    published_at: datetime
    author_id: str

class Collection(BaseModel):
    id: str
    title: str
    description: str
    collection_type: CollectionType
    item_ids: List[str] = [] # Ordered list of LibraryItem IDs
    created_at: datetime
    owner_id: str
