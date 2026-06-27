from typing import Dict, List
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import Achievement, AchievementType

logger = getLogger("AchievementEngine")

class AchievementEngine:
    def __init__(self):
        self._achievements: Dict[str, Achievement] = {}

    def get_user_achievements(self, user_id: str) -> List[Achievement]:
        return [ach for ach in self._achievements.values() if ach.user_id == user_id]

    def unlock_achievement(self, user_id: str, achievement_type: AchievementType, title: str, description: str, related_entity_id: str = "") -> Achievement:
        ach = Achievement(
            id=str(uuid.uuid4()),
            user_id=user_id,
            achievement_type=achievement_type,
            title=title,
            description=description,
            unlocked_at=datetime.now(timezone.utc),
            related_entity_id=related_entity_id
        )
        self._achievements[ach.id] = ach
        logger.info(f"User {user_id} unlocked achievement: {title} ({achievement_type.value})")
        return ach
