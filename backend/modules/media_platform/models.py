from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone

class AssetVersion(BaseModel):
    version_id: str = Field(default_factory=lambda: f"ver-{uuid.uuid4().hex[:8]}")
    version_number: int
    file_size_bytes: int
    uploaded_by: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    storage_path: str
    change_summary: Optional[str] = None

class MediaAsset(BaseModel):
    id: str = Field(default_factory=lambda: f"media-{uuid.uuid4().hex[:8]}")
    filename: str
    file_type: str # e.g., 'image/png', 'application/pdf', 'video/mp4'
    title: str
    description: Optional[str] = None
    
    # Metadata & Categorization
    document_type: Optional[str] = None # e.g. SOP, Drawing, Form
    tags: List[str] = Field(default_factory=list)
    ai_keywords: List[str] = Field(default_factory=list)
    
    # Versioning
    current_version: int = 1
    versions: List[AssetVersion] = Field(default_factory=list)
    
    # References to Knowledge Graph
    entity_id: Optional[str] = None # Link to the EnterpriseEntity
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: str

class MediaFilter(BaseModel):
    file_types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    search_query: Optional[str] = None
    limit: int = 50
