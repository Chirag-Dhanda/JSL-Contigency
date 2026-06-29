from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class OntologyConcept(BaseModel):
    """A semantic concept in the ontology."""
    concept_id: str
    display_name: str
    description: Optional[str] = None
    synonyms: List[str] = Field(default_factory=list)
    namespace: str = "core"

class OntologyClassification(BaseModel):
    """Classification tag applied to metadata objects."""
    classification_id: str
    label: str
    concept_ref: str
    namespace: str = "core"

class TaxonomyNode(BaseModel):
    """A hierarchical node in a taxonomy tree."""
    node_id: str
    concept_ref: str
    children: List["TaxonomyNode"] = Field(default_factory=list)

class TaxonomyTree(BaseModel):
    """A full taxonomy hierarchy."""
    taxonomy_id: str
    name: str
    root: TaxonomyNode
