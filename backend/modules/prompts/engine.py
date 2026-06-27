from typing import Dict, Any

class PromptEngine:
    """Composes strict AI prompts preventing injection and ensuring persona compliance."""
    
    def __init__(self):
        self.default_system_prompt = (
            "You are an expert AI assistant for the JSL Enterprise Learning Platform. "
            "You strictly answer questions related to industrial manufacturing, safety, and training. "
            "Do not answer questions outside this scope."
        )
        self.safety_guardrail = (
            "\n[SAFETY PROTOCOL]: If the user asks about dangerous procedures without "
            "proper PPE, you must strictly warn them."
        )

    def get_persona_prompt(self, persona: str) -> str:
        """Returns the specific prompt block for the selected persona."""
        persona_prompts = {
            "SAFETY_EXPERT": "You are a Safety Expert. Prioritize hazard prevention and PPE compliance in all answers.",
            "MANUFACTURING_EXPERT": "You are a Manufacturing Expert. Focus on equipment efficiency, process flow, and output quality.",
            "GENERAL_ASSISTANT": "You are a helpful Learning Assistant."
        }
        return persona_prompts.get(persona, persona_prompts["GENERAL_ASSISTANT"])

    def compile_prompt(self, user_query: str, context: Dict[str, Any], persona: str) -> str:
        """
        Injects the context variables and persona prompt into a structured prompt block 
        before appending the raw user query, protecting the system prompt from injection.
        """
        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
        persona_str = self.get_persona_prompt(persona)
        
        compiled = (
            f"Persona:\n{persona_str}\n\n"
            "Current Environment Context:\n"
            f"{context_str}\n\n"
            "User Query:\n"
            f"{user_query}"
        )
        return compiled
        
    def get_system_prompt(self) -> str:
        return self.default_system_prompt + self.safety_guardrail
