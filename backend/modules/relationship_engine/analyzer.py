from typing import List
from exceptions.base import SystemException
from .neo4j_repository import Neo4jRepository
import logging

logger = logging.getLogger("RelationshipAnalyzer")

class DependencyAnalyzer:
    """
    Analyzes upstream and downstream dependencies using Neo4j graph traversals.
    """
    def __init__(self, repo: Neo4jRepository):
        self.repo = repo

    async def get_impact_radius(self, node_id: str, depth: int = 3) -> dict:
        """Finds all connected entities up to a specific depth to gauge impact of changes."""
        paths = await self.repo.get_neighbors(node_id, max_depth=depth)
        
        impacted_nodes = set()
        for path in paths:
            for node in path["nodes"]:
                if node.get("id") != node_id:
                    impacted_nodes.add(node.get("id"))
                    
        return {
            "root_node": node_id,
            "impact_radius": len(impacted_nodes),
            "impacted_nodes": list(impacted_nodes)
        }
