from typing import List, Dict, Any
from pydantic import BaseModel
from modules.knowledge_index.metadata import DocumentMetadata

class RetrievedPassage(BaseModel):
    id: str
    text: str
    score: float
    metadata: DocumentMetadata

class AIContextPackage(BaseModel):
    passages: List[RetrievedPassage]
    collection_searched: str
    total_found: int
    related_resources: List[str] = []
    
    def format_for_prompt(self) -> str:
        """Helper to quickly serialize the passages for the AI PromptEngine."""
        if not self.passages:
            return "No relevant internal knowledge found."
            
        formatted = "--- RELEVANT INTERNAL KNOWLEDGE ---\n"
        for i, passage in enumerate(self.passages):
            formatted += f"[{i+1}] Source: {passage.metadata.document_source} (v{passage.metadata.version})\n"
            formatted += f"Text: {passage.text}\n\n"
        formatted += "-----------------------------------"
        
        return formatted
