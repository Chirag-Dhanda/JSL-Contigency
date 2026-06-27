from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

class DomainEvent(BaseModel):
    """Base model for all events broadcast across the enterprise bus."""
    event_id: str
    event_type: str
    timestamp: datetime
    source_module: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    
    @classmethod
    def create(cls, event_type: str, source: str, payload: Dict[str, Any], correlation_id: Optional[str] = None):
        return cls(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            source_module=source,
            payload=payload,
            correlation_id=correlation_id
        )
