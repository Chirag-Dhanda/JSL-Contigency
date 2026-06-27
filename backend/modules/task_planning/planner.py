import logging
from typing import Dict, List, Any

logger = logging.getLogger("TaskPlanner")

class TaskPlanner:
    """Analyzes complex queries and breaks them into an Execution Graph."""
    
    def __init__(self):
        pass

    def create_execution_graph(self, query: str) -> List[Dict[str, Any]]:
        """Parses intent and maps to required agents."""
        logger.info(f"Planning task for query: '{query}'")
        
        graph = []
        query_lower = query.lower()
        
        # Naive intent routing for demonstration
        if "equipment" in query_lower or "spec" in query_lower:
            graph.append({
                "step": len(graph) + 1,
                "agent_id": "mfg_expert",
                "task": "Extract equipment specifications"
            })
            
        if "safety" in query_lower or "hazard" in query_lower:
            graph.append({
                "step": len(graph) + 1,
                "agent_id": "safety_expert",
                "task": "Extract safety protocols"
            })
            
        if not graph:
            # Fallback
            graph.append({
                "step": 1,
                "agent_id": "mfg_expert",
                "task": "General response"
            })
            
        return graph
