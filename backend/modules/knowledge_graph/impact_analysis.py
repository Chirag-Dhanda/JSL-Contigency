import logging
from typing import Dict, List, Any
from .graph import GraphEngine
from modules.entity_framework.models import EnterpriseEntity

logger = logging.getLogger("ImpactAnalysis")

class ImpactAnalysisEngine:
    """
    Determines the cascading effect of changing an entity.
    Example: Modifying an SOP should flag related Training Lessons and Equipment.
    """
    
    def __init__(self, graph_engine: GraphEngine):
        self.graph = graph_engine
        
    def analyze_change_impact(self, entity_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Runs a traversal to identify dependencies.
        Returns a dictionary grouped by Entity Type.
        """
        logger.info(f"Running Change Impact Analysis for {entity_id}")
        
        # We traverse OUTWARD along dependencies, or INWARD along things that depend on this
        # For a generalized impact analysis, we search bidirectionally for 2 hops.
        impacted_entities = self.graph.traverse_bfs(entity_id, max_depth=2)
        
        impact_report = {}
        for entity in impacted_entities:
            e_type = entity.entity_type
            if e_type not in impact_report:
                impact_report[e_type] = []
                
            impact_report[e_type].append({
                "id": entity.id,
                "name": entity.name,
                "display_name": entity.display_name,
                "status": entity.status.value
            })
            
        logger.info(f"Impact Analysis Complete. Found {len(impacted_entities)} impacted entities.")
        return impact_report
