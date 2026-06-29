"""
Base AI Skill interface (EP-08).
"""
from abc import ABC, abstractmethod
from typing import Optional

from modules.search_engine.models import ContextPackage
from modules.ai_platform.models import AIChatRequest, AIChatResponse


class BaseAISkill(ABC):
    @property
    @abstractmethod
    def skill_id(self) -> str:
        """Unique identifier for this skill."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this skill does."""
        ...

    @abstractmethod
    async def execute(
        self,
        request: AIChatRequest,
        context_package: Optional[ContextPackage]
    ) -> AIChatResponse:
        """Execute the skill and return a response."""
        ...
