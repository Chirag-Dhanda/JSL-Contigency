from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class EmbeddingMetadata(BaseModel):
    """
    Standardized metadata schema for all enterprise embeddings.
    """
    embedding_id: str = Field(..., description="Unique identifier for the embedding chunk")
    document_id: str = Field(..., description="ID of the parent document")
    chunk_id: int = Field(..., description="Sequential chunk index within the document")
    department: str = Field(..., description="Department owner of the knowledge")
    collection: str = Field(..., description="Target ChromaDB collection (e.g. safety, manufacturing)")
    knowledge_type: str = Field(..., description="Type of knowledge (SOP, Policy, Lesson, etc.)")
    version: str = Field(..., description="Document version string")
    author: str = Field(..., description="Original author or system")
    language: str = Field(default="en", description="Language code")
    security_level: int = Field(default=0, description="Clearance level required to access (0-5)")
    source_document: str = Field(..., description="Path or URI to original document")
    creation_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="When this embedding was created")
    embedding_model: str = Field(..., description="Model used to generate embedding")
    embedding_version: str = Field(default="1.0", description="Version of the embedding pipeline")

class EmbeddingRequest(BaseModel):
    """Request to queue a document chunk for embedding."""
    content: str
    metadata: EmbeddingMetadata

class EmbeddingResponse(BaseModel):
    """Response after a successful embedding."""
    embedding_id: str
    status: str = "success"
    model_used: str
    latency_ms: int
