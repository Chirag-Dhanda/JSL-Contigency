from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from .enums import MediaType

class MediaAsset(BaseModel):
    id: str
    filename: str
    media_type: MediaType
    url: str
    size_bytes: int
    mime_type: str
    uploaded_by_user_id: str
    uploaded_at: datetime
    
    # Used for AI tagging or SCORM linkage later
    metadata: Dict[str, str] = {}
    is_archived: bool = False
