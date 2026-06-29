"""
DI Registration for Enterprise AI Orchestration Platform (EP-08).
"""
import logging
from typing import Any

from core.module import BaseModule
from core.di import container

from modules.ai.client import OllamaClient
from modules.search_engine.service import EnterpriseSearchService

from .providers.ollama_provider import OllamaProvider
from .providers.provider_registry import ProviderRegistry
from .prompt_engine import PromptAssemblyEngine
from .context_guard import EnterpriseContextGuard
from .validation import ResponseValidationEngine
from .citations import CitationInjectionEngine
from .conversation import ConversationService
from .observability import AIObservabilityService
from .orchestrator import AIOrchestrator
from .tools import EnterpriseToolRegistry, EnterpriseTool
from .recommendations import AIRecommendationEngine
from .skills.skill_registry import SkillRegistry
from .skills.builtin_skills import ALL_BUILTIN_SKILLS

logger = logging.getLogger("AIOrchestrationModule")


class AIOrchestrationModule(BaseModule):
    """Registers all Enterprise AI Platform services with the DI container."""

    @property
    def name(self) -> str:
        return "AIOrchestrationPlatform"

    @property
    def version(self) -> str:
        return "1.0.0"

    def register_services(self, container: Any) -> None:
        logger.info("Registering AI Orchestration Platform (EP-08) services...")

        # ── Provider Layer ───────────────────────────────────────────
        ollama_client = OllamaClient()
        ollama_provider = OllamaProvider(client=ollama_client)

        provider_registry = ProviderRegistry(default_provider="ollama")
        provider_registry.register(ollama_provider)
        container.register_singleton(ProviderRegistry, provider_registry)

        # ── Core Services ────────────────────────────────────────────
        prompt_engine = PromptAssemblyEngine()
        container.register_singleton(PromptAssemblyEngine, prompt_engine)

        context_guard = EnterpriseContextGuard()
        container.register_singleton(EnterpriseContextGuard, context_guard)

        validator = ResponseValidationEngine()
        container.register_singleton(ResponseValidationEngine, validator)

        citation_engine = CitationInjectionEngine()
        container.register_singleton(CitationInjectionEngine, citation_engine)

        conversation_svc = ConversationService()
        container.register_singleton(ConversationService, conversation_svc)

        observability = AIObservabilityService()
        container.register_singleton(AIObservabilityService, observability)

        # ── Orchestrator ─────────────────────────────────────────────
        search_svc = container.resolve(EnterpriseSearchService)
        orchestrator = AIOrchestrator(
            provider_registry=provider_registry,
            search_service=search_svc,
            prompt_engine=prompt_engine,
            context_guard=context_guard,
            validator=validator,
            citation_engine=citation_engine,
            conversation_service=conversation_svc,
            observability=observability
        )
        container.register_singleton(AIOrchestrator, orchestrator)

        # ── Skills ───────────────────────────────────────────────────
        skill_registry = SkillRegistry()
        for SkillClass in ALL_BUILTIN_SKILLS:
            skill = SkillClass()
            skill.bind_orchestrator(orchestrator)
            skill_registry.register(skill)
        container.register_singleton(SkillRegistry, skill_registry)

        # ── Tool Registry (with safe enterprise tools) ───────────────
        tool_registry = EnterpriseToolRegistry()
        # Register Search Tool (permission: all users)
        tool_registry.register(
            EnterpriseTool("search", "Query enterprise knowledge base", required_roles=[]),
            handler=lambda query: search_svc.execute_search(
                __import__("modules.search_engine.models", fromlist=["SearchRequest"]).SearchRequest(query=query)
            )
        )
        container.register_singleton(EnterpriseToolRegistry, tool_registry)

        # ── Recommendation Engine ────────────────────────────────────
        rec_engine = AIRecommendationEngine()
        container.register_singleton(AIRecommendationEngine, rec_engine)

    async def initialize(self) -> None:
        logger.info("AI Orchestration Platform initialized.")

    async def shutdown(self) -> None:
        pass
