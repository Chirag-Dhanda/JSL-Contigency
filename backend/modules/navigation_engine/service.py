import logging
from typing import Dict, List, Any
from modules.knowledge_graph.graph import GraphEngine

logger = logging.getLogger("NavigationEngine")

class DynamicNavigationEngine:
    """
    Generates hierarchical UI navigation trees dynamically from the Knowledge Graph.
    Instead of hardcoded menus, this crawls relationships like 'contains' or 'belongs_to'.
    """
    
    def __init__(self, graph_engine: GraphEngine):
        self.graph = graph_engine
        logger.info("Navigation Engine Initialized.")
        
    def generate_hierarchy(self, root_entity_id: str, edge_type: str = "contains", depth: int = 3) -> Dict[str, Any]:
        """
        Recursively builds a tree structure starting from a root node,
        following a specific edge type (e.g., 'contains').
        """
        try:
            # We fetch the entity to get its name for the tree
            root_entity = self.graph.metadata_engine.get_entity(root_entity_id)
        except Exception:
            return {"error": "Root entity not found"}
            
        tree = {
            "id": root_entity.id,
            "name": root_entity.display_name,
            "type": root_entity.entity_type,
            "children": []
        }
        
        if depth > 0:
            # Find entities that this root 'contains' (Root -> contains -> Child)
            # This means we traverse OUTWARD on the 'contains' edge.
            children = self.graph.get_neighbours(root_entity_id, edge_types=[edge_type], direction="OUT")
            
            for child in children:
                # Recursively build the branch
                child_tree = self.generate_hierarchy(child.id, edge_type, depth - 1)
                tree["children"].append(child_tree)
                
        return tree
