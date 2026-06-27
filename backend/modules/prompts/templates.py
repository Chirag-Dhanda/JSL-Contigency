from pydantic import BaseModel, Field
from typing import List, Optional

class PromptTemplate(BaseModel):
    name: str = Field(description="Name of the prompt template")
    system_prompt: str = Field(description="Base system instructions")
    role_prompt: str = Field(description="Role specific instructions")
    safety_prompt: str = Field(description="Safety instructions")
    manufacturing_prompt: str = Field(description="Domain-specific instructions")
    variables: List[str] = Field(default_factory=list, description="Expected variables in the prompt")

class StandardTemplates:
    GENERAL_ASSISTANT = PromptTemplate(
        name="general_assistant",
        system_prompt="You are an enterprise AI assistant for JSL Contingency.",
        role_prompt="Your role is to assist users accurately and efficiently.",
        safety_prompt="Do not reveal internal system details or credentials. Maintain professional tone.",
        manufacturing_prompt="Use standard manufacturing terminology where applicable.",
        variables=["context", "user_query"]
    )
    
    # Future templates can be added here (e.g., Code Assistant, Data Analyst, etc.)
