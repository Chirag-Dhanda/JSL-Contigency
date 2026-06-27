import logging
from typing import List, Dict, Any
from modules.knowledge_extraction.models import ExtractedEntity

logger = logging.getLogger("EntityRelationshipDetector")

class EntityRelationshipDetector:
    """Analyzes extracted entities to form relational edges for the Knowledge Graph."""
    
    def __init__(self):
        pass
        
    def detect_relationships(self, entities: List[ExtractedEntity], document_class: str) -> List[Dict[str, Any]]:
        """
        Determines relationships between entities and their source document.
        """
        logger.debug("Detecting entity relationships...")
        
        relationships = []
        for entity in entities:
            # Example relationship: "Electric Arc Furnace" is the SUBJECT of this "SOP"
            rel = {
                "source": entity.entity_value,
                "target": entity.document_reference_id,
                "relationship_type": f"IS_SUBJECT_OF_{document_class.upper().replace(' ', '_')}",
                "confidence": entity.confidence_score
            }
            relationships.append(rel)
            
        return relationships
