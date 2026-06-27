from typing import Optional, List, Dict
from pydantic import BaseModel

class LearningMaterial(BaseModel):
    id: str
    title: str
    content_url: Optional[str] = None
    time_estimate_mins: int = 15

class AssessmentPlaceholder(BaseModel):
    id: str
    title: str
    passing_score: float = 80.0

# --- Manufacturing Learning Integration ---

class KnowledgeCard(BaseModel):
    id: str
    title: str
    content: str
    is_safety_critical: bool = False

class InteractiveDiagram(BaseModel):
    id: str
    image_url: str
    clickable_components: List[str]

class StationLesson(BaseModel):
    id: str
    station_id: str
    title: str
    knowledge_cards: List[KnowledgeCard] = []
    diagrams: List[InteractiveDiagram] = []

class LearningExperience(BaseModel):
    id: str
    knowledge_object_id: str
    overview: str = ""
    objectives: List[str] = []
    learning_content: Dict[str, str] = {}
    important_notes: List[str] = []
    warnings: List[str] = []
    safety_alerts: List[str] = []
    knowledge_check_ids: List[str] = []
    summary: str = ""
    related_topics_ids: List[str] = []
    references: List[str] = []
    ai_chat_enabled: bool = False
