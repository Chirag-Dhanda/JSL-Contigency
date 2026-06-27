import logging
from typing import Dict, Any, List

logger = logging.getLogger("GraphPreparer")

class GraphPreparer:
    """Foundational class that formats entities and relationships into node/edge schemas."""
    
    def __init__(self):
        pass
        
    def prepare_graph_payload(self, entities: List[Any], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepares the payload for future ingestion into a Graph Database (like Neo4j).
        """
        logger.debug("Preparing Knowledge Graph payload...")
        
        nodes = [{"id": e.entity_value, "label": e.entity_type, "properties": e.properties} for e in entities]
        edges = relationships
        
        return {
            "nodes": nodes,
            "edges": edges
        }
