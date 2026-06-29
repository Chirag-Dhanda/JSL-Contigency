"""
Skill Registry (EP-08).
Manages available AI skills — enable/disable at runtime.
"""
import logging
from typing import Dict, List, Optional
from .base_skill import BaseAISkill

logger = logging.getLogger("AIPlatform.SkillRegistry")


class SkillRegistry:
    """
    Manages the catalogue of enterprise AI skills.
    Skills can be enabled/disabled without code changes.
    """

    def __init__(self):
        self._skills: Dict[str, BaseAISkill] = {}
        self._disabled: set = set()

    def register(self, skill: BaseAISkill) -> None:
        self._skills[skill.skill_id] = skill
        logger.info(f"Registered AI skill: '{skill.skill_id}'")

    def resolve(self, skill_id: str) -> Optional[BaseAISkill]:
        if skill_id in self._disabled:
            raise PermissionError(f"Skill '{skill_id}' is currently disabled.")
        return self._skills.get(skill_id)

    def enable(self, skill_id: str) -> None:
        self._disabled.discard(skill_id)

    def disable(self, skill_id: str) -> None:
        self._disabled.add(skill_id)
        logger.info(f"Disabled AI skill: '{skill_id}'")

    def list_skills(self) -> List[Dict]:
        return [
            {
                "skill_id": s.skill_id,
                "description": s.description,
                "enabled": s.skill_id not in self._disabled
            }
            for s in self._skills.values()
        ]
