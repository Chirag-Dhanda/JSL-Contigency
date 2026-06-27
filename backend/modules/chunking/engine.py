from typing import List
from pydantic import BaseModel

from modules.knowledge_index.metadata import DocumentMetadata

class DocumentChunk(BaseModel):
    chunk_index: int
    text: str
    metadata: DocumentMetadata
    
class ChunkingEngine:
    """Slices a massive document string into optimized overlapping chunks."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk_document(self, text: str, metadata: DocumentMetadata) -> List[DocumentChunk]:
        """
        Basic character/word splitting. 
        In production, this might use semantic splitting (e.g., recursive character text splitters).
        """
        words = text.split()
        chunks = []
        
        if not words:
            return chunks
            
        i = 0
        chunk_index = 0
        while i < len(words):
            end_index = min(i + self.chunk_size, len(words))
            chunk_text = " ".join(words[i:end_index])
            
            # Every chunk receives an exact copy of the parent document's metadata
            chunk = DocumentChunk(
                chunk_index=chunk_index,
                text=chunk_text,
                metadata=metadata
            )
            chunks.append(chunk)
            
            # Step forward by chunk_size minus the overlap
            i += (self.chunk_size - self.overlap)
            chunk_index += 1
            
            if i >= len(words):
                break
                
        return chunks
