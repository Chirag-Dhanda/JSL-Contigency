from pydantic import BaseModel
from datetime import datetime

from .enums import AchievementType

class Achievement(BaseModel):
    id: str
    user_id: str
    achievement_type: AchievementType
    title: str
    description: str
    icon_url: str = ""
    unlocked_at: datetime
    related_entity_id: str = "" # e.g., the lesson or assessment ID that triggered it
