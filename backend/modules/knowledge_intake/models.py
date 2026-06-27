from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class ProposedEntity(BaseModel):
    id: str = Field(default_factory=lambda: f"prop-ent-{uuid.uuid4().hex[:8]}")
    entity_type: str
    display_name: str
    proposed_metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 1.0
    status: str = "PENDING" # PENDING, APPROVED, REJECTED

class ProposedRelationship(BaseModel):
    id: str = Field(default_factory=lambda: f"prop-rel-{uuid.uuid4().hex[:8]}")
    source_id: str
    target_id: str # Can be an existing entity ID or another proposed entity ID
    relationship_type: str
    confidence_score: float = 1.0

class IntakeJob(BaseModel):
    id: str = Field(default_factory=lambda: f"job-{uuid.uuid4().hex[:8]}")
    filename: str
    file_type: str
    uploaded_by: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "PROCESSING" # PROCESSING, IN_REVIEW, COMPLETED, FAILED
    
    # Document Understanding
    document_type: Optional[str] = None
    extracted_text: Optional[str] = None
    language: str = "en"
    
    # Architect Proposals
    proposed_entities: List[ProposedEntity] = Field(default_factory=list)
    proposed_relationships: List[ProposedRelationship] = Field(default_factory=list)
    
    # AI Summary
    ai_summary: str = ""
    sap_placeholders_created: int = 0
