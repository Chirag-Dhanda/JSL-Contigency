"""
Built-in AI Skills (EP-08).
Each skill delegates to the AI Orchestrator — no skill talks directly to an LLM.
Skills are thin wrappers that customise the request before passing it up.
"""
import logging
from typing import Optional

from modules.search_engine.models import ContextPackage
from modules.ai_platform.models import AIChatRequest, AIChatResponse
from .base_skill import BaseAISkill

logger = logging.getLogger("AIPlatform.Skills")


# ─────────────────────────────────────────────
# Base Orchestrator-Delegating Skill
# (avoids circular import by accepting orchestrator at runtime)
# ─────────────────────────────────────────────

class _OrchestratorDelegatingSkill(BaseAISkill):
    """Internal base: injects orchestrator post-construction to avoid circular deps."""
    def __init__(self):
        self._orchestrator = None  # Set by module.py after all services are wired

    def bind_orchestrator(self, orchestrator) -> None:
        self._orchestrator = orchestrator

    async def execute(self, request: AIChatRequest, context_package: Optional[ContextPackage]) -> AIChatResponse:
        if self._orchestrator is None:
            raise RuntimeError(f"Skill '{self.skill_id}' orchestrator not bound.")
        # Override skill in request to match this skill's ID
        patched = request.model_copy(update={"skill": self.skill_id})
        return await self._orchestrator.chat(patched)


class KnowledgeQASkill(_OrchestratorDelegatingSkill):
    @property
    def skill_id(self) -> str:
        return "knowledge_qa"

    @property
    def description(self) -> str:
        return "Answers questions using enterprise knowledge, with source citations."


class DocumentSummarySkill(_OrchestratorDelegatingSkill):
    @property
    def skill_id(self) -> str:
        return "document_summary"

    @property
    def description(self) -> str:
        return "Summarizes enterprise documents from the Knowledge Repository."


class MetadataExplainSkill(_OrchestratorDelegatingSkill):
    @property
    def skill_id(self) -> str:
        return "metadata_explain"

    @property
    def description(self) -> str:
        return "Explains enterprise object metadata, attributes, and relationships."


class WorkflowGuidanceSkill(_OrchestratorDelegatingSkill):
    @property
    def skill_id(self) -> str:
        return "workflow_guidance"

    @property
    def description(self) -> str:
        return "Guides users through active enterprise workflow steps."


class SearchAssistSkill(_OrchestratorDelegatingSkill):
    @property
    def skill_id(self) -> str:
        return "search_assist"

    @property
    def description(self) -> str:
        return "Refines enterprise search queries and suggests related concepts."


# Convenience list for registration
ALL_BUILTIN_SKILLS = [
    KnowledgeQASkill,
    DocumentSummarySkill,
    MetadataExplainSkill,
    WorkflowGuidanceSkill,
    SearchAssistSkill,
]
