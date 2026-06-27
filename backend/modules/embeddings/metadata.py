from pydantic import BaseModel
from typing import Optional
from modules.knowledge_index.metadata import DocumentMetadata

class EmbeddingMetadata(BaseModel):
    """Wraps DocumentMetadata with Vector-specific properties."""
    embedding_id: str
    document_id: str
    chunk_id: str
    document_metadata: DocumentMetadata
    embedding_model: str
    embedding_version: str
    creation_timestamp: str
