from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from .enums import ProgressStatus, EntityType

class ProgressRecord(BaseModel):
    id: str
    user_id: str
    entity_id: str
    entity_type: EntityType
    
    # Core Metrics
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    completion_percentage: float = 0.0
    time_spent_mins: int = 0
    average_session_mins: float = 0.0
    
    # Roadmap / Collection specific
    skipped_lessons: List[str] = []
    mandatory: bool = False
    
    # Assessment specific
    attempts: int = 0
    pass_rate: float = 0.0 # Pass rate if multiple assessments are aggregated, or 1.0/0.0 for single
    
    last_accessed: datetime
    completed_at: Optional[datetime] = None
