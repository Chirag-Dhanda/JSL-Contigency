from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime

from .enums import CompetencyArea

class CompetencyProfile(BaseModel):
    user_id: str
    overall_readiness_score: float = 0.0
    area_scores: Dict[CompetencyArea, float] = {} # Area to percentage score
    completed_assessments: List[str] = []
    last_updated: datetime
