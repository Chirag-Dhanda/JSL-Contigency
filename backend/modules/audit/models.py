from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class AuditEvent(BaseModel):
    """Immutable record of an enterprise action."""
    id: str
    action: str
    actor_id: str
    target_resource_id: Optional[str] = None
    timestamp: datetime
    metadata_snapshot: Dict[str, Any] = {}
