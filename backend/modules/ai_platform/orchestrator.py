"""
AI Orchestrator (EP-08).
Central service orchestrating the full AI request lifecycle.

Request Flow:
  AIChatRequest
    → ConversationService (get/create session)
    → EnterpriseSearchService (retrieve ContextPackage)
    → EnterpriseContextGuard (permission filter)
    → PromptAssemblyEngine (build prompt from template)
    → ProviderRegistry (select LLM)
    → BaseLLMProvider.generate()
    → ResponseValidationEngine (validate)
    → CitationInjectionEngine (inject sources)
    → ConversationService (persist turn)
    → AIObservabilityService (record metrics)
    → AIChatResponse

No client communicates directly with an LLM provider.
"""
import logging
import time
from typing import Optional

from modules.search_engine.service import EnterpriseSearchService
from modules.search_engine.models import SearchRequest, ContextPackage
from .models import AIChatRequest, AIChatResponse, ConversationTurn
from .providers.provider_registry import ProviderRegistry
from .prompt_engine import PromptAssemblyEngine
from .context_guard import EnterpriseContextGuard
from .validation import ResponseValidationEngine
from .citations import CitationInjectionEngine
from .conversation import ConversationService
from .observability import AIObservabilityService

logger = logging.getLogger("AIPlatform.Orchestrator")


class AIOrchestrator:
    """
    The central intelligence gateway for EKOS.
    All AI interactions must pass through this class.
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        search_service: EnterpriseSearchService,
        prompt_engine: PromptAssemblyEngine,
        context_guard: EnterpriseContextGuard,
        validator: ResponseValidationEngine,
        citation_engine: CitationInjectionEngine,
        conversation_service: ConversationService,
        observability: AIObservabilityService,
    ):
        self.providers = provider_registry
        self.search = search_service
        self.prompt_engine = prompt_engine
        self.context_guard = context_guard
        self.validator = validator
        self.citation_engine = citation_engine
        self.conversations = conversation_service
        self.observability = observability

    async def chat(self, request: AIChatRequest) -> AIChatResponse:
        t_start = time.monotonic()

        # 1. Resolve/create conversation
        user_id = "system"  # In full implementation, extracted from auth context
        conversation = self.conversations.get_or_create(
            request.conversation_id, user_id=user_id
        )
        history = self.conversations.get_history(conversation.conversation_id)

        # 2. Retrieve enterprise context via Search & Context Engine (EP-06)
        context_package: Optional[ContextPackage] = None
        try:
            search_req = SearchRequest(
                query=request.query,
                user_department=request.user_department,
                user_roles=request.user_roles,
                max_results=8,
                include_graph_expansion=True
            )
            context_package = await self.search.execute_search(search_req)
        except Exception as e:
            logger.warning(f"Context retrieval failed: {e}. Proceeding with empty context.")

        # 3. Context Guard — enforce permissions before prompt assembly
        safe_context: Optional[ContextPackage] = None
        if context_package:
            try:
                safe_context = self.context_guard.validate_and_sanitize(request, context_package)
            except Exception as e:
                logger.error(f"Context Guard raised: {e}")
                safe_context = None

        # 4. Prompt Assembly
        assembled = self.prompt_engine.assemble(
            skill=request.skill,
            query=request.query,
            context_package=safe_context,
            user_role=request.user_roles[0] if request.user_roles else "USER",
            department=request.user_department or "GENERAL",
            conversation_history=history
        )

        # 5. Provider Selection & Generation
        provider = self.providers.resolve()
        llm_response = await provider.generate(
            user_prompt=assembled.user_prompt,
            system_prompt=assembled.system_prompt,
            options=request.options
        )

        # 6. Response Validation
        has_passages = bool(safe_context and safe_context.passages)
        validation = self.validator.validate(llm_response, context_had_passages=has_passages)

        if not validation.passed:
            final_text = self.validator.safe_response(validation)
        else:
            final_text = llm_response.raw_text

        # 7. Citation Injection
        annotated_text, structured_citations = self.citation_engine.inject(
            final_text, safe_context
        )

        # 8. Persist conversation turns
        user_turn = ConversationTurn(
            role="user",
            content=request.query,
            skill=request.skill
        )
        assistant_turn = ConversationTurn(
            role="assistant",
            content=annotated_text,
            skill=request.skill,
            prompt_template_id=assembled.template_id,
            provider=provider.provider_name,
            model=llm_response.model,
            citation_ids=[c["citation_id"] for c in structured_citations if "citation_id" in c]
        )
        self.conversations.append_turn(conversation.conversation_id, user_turn)
        self.conversations.append_turn(conversation.conversation_id, assistant_turn)

        latency_ms = (time.monotonic() - t_start) * 1000

        # 9. Observability
        self.observability.record(
            conversation_id=conversation.conversation_id,
            turn_id=assistant_turn.turn_id,
            skill=request.skill,
            provider=provider.provider_name,
            model=llm_response.model,
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            total_tokens=llm_response.total_tokens,
            latency_ms=latency_ms,
            context_passages=len(safe_context.passages) if safe_context else 0,
            citations_injected=len(structured_citations),
            validation_passed=validation.passed
        )

        return AIChatResponse(
            conversation_id=conversation.conversation_id,
            turn_id=assistant_turn.turn_id,
            answer=annotated_text,
            citations=structured_citations,
            skill=request.skill,
            provider=provider.provider_name,
            model=llm_response.model,
            validation_passed=validation.passed,
            validation_notes=validation.issues,
            tokens_used=llm_response.total_tokens,
            latency_ms=round(latency_ms, 2)
        )
