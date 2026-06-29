"""
Prompt Assembly Engine (EP-08).
Assembles versioned, enterprise-aware prompts from templates.
"""
import logging
from typing import Optional, List, Dict, Any

from modules.search_engine.models import ContextPackage
from .models import PromptTemplate, AssembledPrompt, ConversationTurn

logger = logging.getLogger("AIPlatform.PromptEngine")

# ─────────────────────────────────────────────
# Built-in versioned prompt templates (future: stored in DB)
# ─────────────────────────────────────────────
_BUILTIN_TEMPLATES: Dict[str, PromptTemplate] = {}

def _register(t: PromptTemplate):
    _BUILTIN_TEMPLATES[t.skill] = t

_register(PromptTemplate(
    name="Knowledge Q&A",
    version=1,
    skill="knowledge_qa",
    system_template=(
        "You are an enterprise knowledge assistant for {department}.\n"
        "You ONLY answer based on the provided enterprise context.\n"
        "Every factual claim MUST reference a provided source by its [Source N] label.\n"
        "If the context does not contain enough information, state that clearly.\n"
        "Role: {role}. Never guess or hallucinate."
    ),
    user_template=(
        "Enterprise Context:\n{context}\n\n"
        "Conversation History:\n{history}\n\n"
        "Question: {query}"
    )
))

_register(PromptTemplate(
    name="Document Summary",
    version=1,
    skill="document_summary",
    system_template=(
        "You are a document summarization assistant for {department}.\n"
        "Summarize the following enterprise document content concisely and accurately.\n"
        "Do not include information not present in the document.\n"
        "Role: {role}."
    ),
    user_template=(
        "Document Content:\n{context}\n\n"
        "Provide a structured summary:"
    )
))

_register(PromptTemplate(
    name="Workflow Guidance",
    version=1,
    skill="workflow_guidance",
    system_template=(
        "You are an enterprise process assistant.\n"
        "Guide the user through the current workflow step based on enterprise process definitions.\n"
        "Do not execute any steps automatically.\n"
        "Role: {role}. Department: {department}."
    ),
    user_template=(
        "Current Workflow State:\n{context}\n\n"
        "User Question: {query}"
    )
))

_register(PromptTemplate(
    name="Search Assist",
    version=1,
    skill="search_assist",
    system_template=(
        "You are an enterprise search assistant.\n"
        "Help the user refine their query based on available enterprise knowledge.\n"
        "Suggest related concepts but do not fabricate information.\n"
        "Role: {role}."
    ),
    user_template=(
        "Retrieved Results Summary:\n{context}\n\n"
        "User Query: {query}\n\n"
        "Provide search improvement suggestions:"
    )
))


class PromptAssemblyEngine:
    """
    Assembles prompts from versioned templates, binding enterprise context.
    """
    CHARS_PER_TOKEN = 4

    def __init__(self):
        self._templates = _BUILTIN_TEMPLATES

    def get_template(self, skill: str) -> PromptTemplate:
        tmpl = self._templates.get(skill)
        if not tmpl:
            logger.warning(f"No template for skill '{skill}', using knowledge_qa fallback.")
            tmpl = self._templates["knowledge_qa"]
        return tmpl

    def assemble(
        self,
        skill: str,
        query: str,
        context_package: Optional[ContextPackage],
        user_role: str = "USER",
        department: str = "GENERAL",
        conversation_history: Optional[List[ConversationTurn]] = None
    ) -> AssembledPrompt:
        tmpl = self.get_template(skill)

        # Format context passages with source labels
        if context_package and context_package.passages:
            ctx_text = "\n\n".join(
                f"[Source {i+1}] ({p.asset_title}): {p.text}"
                for i, p in enumerate(context_package.passages)
            )
        else:
            ctx_text = "No enterprise context available."

        # Format conversation history
        hist_text = ""
        if conversation_history:
            hist_text = "\n".join(
                f"{t.role.capitalize()}: {t.content}" for t in conversation_history[-6:]
            )

        system = tmpl.system_template.format(
            role=user_role, department=department, query=query
        )
        user = tmpl.user_template.format(
            context=ctx_text, query=query, history=hist_text,
            role=user_role, department=department
        )

        estimated_tokens = (len(system) + len(user)) // self.CHARS_PER_TOKEN

        return AssembledPrompt(
            template_id=tmpl.template_id,
            template_version=tmpl.version,
            system_prompt=system,
            user_prompt=user,
            estimated_tokens=estimated_tokens
        )
