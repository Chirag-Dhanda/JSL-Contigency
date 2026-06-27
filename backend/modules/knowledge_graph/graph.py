import logging
from typing import Dict, List, Set
from modules.relationship_engine.service import RelationshipEngineService
from modules.metadata_engine.service import MetadataEngineService
from modules.entity_framework.models import EnterpriseEntity
from exceptions.base import NotFoundException

logger = logging.getLogger("KnowledgeGraph")

class GraphEngine:
    """
    Database-independent Knowledge Graph abstraction.
    Provides graph traversal over the Entity Framework and Relationship Engine.
    """
    def __init__(self, metadata_engine: MetadataEngineService, relationship_engine: RelationshipEngineService):
        self.metadata_engine = metadata_engine
        self.relationship_engine = relationship_engine
        logger.info("Knowledge Graph Engine Initialized.")

    def get_neighbours(self, entity_id: str, edge_types: List[str] = None, direction: str = "BOTH") -> List[EnterpriseEntity]:
        """Finds all directly connected entities."""
        relationships = self.relationship_engine.get_relationships_for_entity(entity_id, direction)
        
        if edge_types:
            relationships = [r for r in relationships if r.relationship_type in edge_types]
            
        neighbours = []
        for rel in relationships:
            target_id = rel.target_entity_id if rel.source_entity_id == entity_id else rel.source_entity_id
            try:
                neighbours.append(self.metadata_engine.get_entity(target_id))
            except NotFoundException:
                logger.warning(f"Graph Integrity Warning: Relationship {rel.id} points to missing entity {target_id}")
                
        return neighbours

    def traverse_bfs(self, start_entity_id: str, max_depth: int = 3, edge_types: List[str] = None) -> List[EnterpriseEntity]:
        """Performs a Breadth-First Search to find connected entities up to a certain depth."""
        visited: Set[str] = set([start_entity_id])
        queue = [(start_entity_id, 0)]
        results = []
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
                
            neighbours = self.get_neighbours(current_id, edge_types=edge_types, direction="OUT")
            for neighbour in neighbours:
                if neighbour.id not in visited:
                    visited.add(neighbour.id)
                    results.append(neighbour)
                    queue.append((neighbour.id, depth + 1))
                    
        return results
