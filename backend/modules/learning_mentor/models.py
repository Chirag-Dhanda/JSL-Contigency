from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class PersonalLearningProfile(BaseModel):
    """Stores the learning state of an employee."""
    user_id: str
    role: str
    department: str
    
    # Progress Tracking
    completed_lessons: List[str] = Field(default_factory=list)
    completed_sops: List[str] = Field(default_factory=list)
    completed_assessments: List[str] = Field(default_factory=list)
    certificates: List[str] = Field(default_factory=list)
    
    # Competency Analysis (Strictly Learning, not HR Performance)
    competencies: Dict[str, float] = Field(default_factory=dict, description="e.g. {'safety': 0.8, 'equipment': 0.4}")
    weak_areas: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    learning_preferences: Dict[str, str] = Field(default_factory=dict)
