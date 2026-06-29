import logging
from typing import Dict, List, Optional
from exceptions.base import NotFoundException
from .models import OntologyConcept, OntologyClassification, TaxonomyTree

logger = logging.getLogger("OntologyRegistry")

class OntologyRegistryService:
    """
    Manages semantic concepts, classifications, and taxonomies without hardcoding business ontology.
    """
    
    def __init__(self):
        self._concepts: Dict[str, OntologyConcept] = {}
        self._classifications: Dict[str, OntologyClassification] = {}
        self._taxonomies: Dict[str, TaxonomyTree] = {}
        logger.info("Ontology Registry Service Initialized.")

    # -- Concepts --
    def register_concept(self, concept: OntologyConcept) -> OntologyConcept:
        self._concepts[concept.concept_id] = concept
        logger.debug(f"Registered Concept: {concept.concept_id}")
        return concept

    def get_concept(self, concept_id: str) -> OntologyConcept:
        if concept_id not in self._concepts:
            raise NotFoundException(message=f"Ontology concept {concept_id} not found.")
        return self._concepts[concept_id]

    def list_concepts(self) -> List[OntologyConcept]:
        return list(self._concepts.values())

    # -- Classifications --
    def register_classification(self, classification: OntologyClassification) -> OntologyClassification:
        self._classifications[classification.classification_id] = classification
        logger.debug(f"Registered Classification: {classification.classification_id}")
        return classification

    def get_classification(self, classification_id: str) -> OntologyClassification:
        if classification_id not in self._classifications:
            raise NotFoundException(message=f"Ontology classification {classification_id} not found.")
        return self._classifications[classification_id]

    # -- Taxonomies --
    def register_taxonomy(self, taxonomy: TaxonomyTree) -> TaxonomyTree:
        self._taxonomies[taxonomy.taxonomy_id] = taxonomy
        logger.debug(f"Registered Taxonomy: {taxonomy.taxonomy_id}")
        return taxonomy
        
    def get_taxonomy(self, taxonomy_id: str) -> TaxonomyTree:
        if taxonomy_id not in self._taxonomies:
            raise NotFoundException(message=f"Taxonomy {taxonomy_id} not found.")
        return self._taxonomies[taxonomy_id]
