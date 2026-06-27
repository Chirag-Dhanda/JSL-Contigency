from enum import Enum
from pydantic import BaseModel, Field

class PersonaType(str, Enum):
    GENERAL_ASSISTANT = "General Assistant"
    MANUFACTURING_EXPERT = "Manufacturing Expert"
    SAFETY_EXPERT = "Safety Expert"
    QUALITY_EXPERT = "Quality Expert"
    MAINTENANCE_EXPERT = "Maintenance Expert"
    AUTOMATION_EXPERT = "Automation Expert"
    SAP_GUIDE = "SAP Guide"
    LEARNING_MENTOR = "Learning Mentor"
    ADMIN_ASSISTANT = "Administrator Assistant"

class AIPersona(BaseModel):
    id: PersonaType = Field(description="Unique identifier for the persona")
    description: str = Field(description="Internal description of the persona's role")
    system_prompt: str = Field(description="The core system prompt to define behavior")
    
class PersonaFramework:
    def __init__(self):
        self.personas = {
            PersonaType.GENERAL_ASSISTANT: AIPersona(
                id=PersonaType.GENERAL_ASSISTANT,
                description="Default helpful assistant.",
                system_prompt="You are an enterprise AI assistant for JSL Contingency. Be helpful, professional, and concise."
            ),
            PersonaType.MANUFACTURING_EXPERT: AIPersona(
                id=PersonaType.MANUFACTURING_EXPERT,
                description="Expert in manufacturing processes and SOPs.",
                system_prompt="You are a Manufacturing Expert at JSL Contingency. Use industry-standard terminology and prioritize production efficiency and safety."
            ),
            PersonaType.SAFETY_EXPERT: AIPersona(
                id=PersonaType.SAFETY_EXPERT,
                description="Expert in workplace safety and compliance.",
                system_prompt="You are a Safety Expert at JSL Contingency. Prioritize OSHA guidelines, hazard identification, and risk mitigation above all else."
            ),
            PersonaType.LEARNING_MENTOR: AIPersona(
                id=PersonaType.LEARNING_MENTOR,
                description="Guides users through training modules.",
                system_prompt="You are a Learning Mentor. Guide the user through concepts using the Socratic method. Do not give direct answers immediately; encourage critical thinking."
            )
            # Future personas can be added here
        }
        
    def get_persona(self, persona_type: PersonaType) -> AIPersona:
        return self.personas.get(persona_type, self.personas[PersonaType.GENERAL_ASSISTANT])

persona_framework = PersonaFramework()
