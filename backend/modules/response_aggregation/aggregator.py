import logging
from typing import Dict, List, Any

logger = logging.getLogger("ResponseAggregator")

class ResponseAggregator:
    """Combines outputs from multiple agents and resolves conflicts."""
    
    def __init__(self):
        pass

    def aggregate(self, execution_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merges results based on priority and deduplication."""
        logger.info(f"Aggregating {len(execution_results)} agent responses.")
        
        combined_text = []
        sources = set()
        highest_priority_agent = None
        
        for result in execution_results:
            agent_id = result.get("agent_id")
            output = result.get("output", "")
            
            combined_text.append(f"[{agent_id.upper()}]: {output}")
            
            # Merge sources
            if "sources" in result:
                sources.update(result["sources"])
                
        final_response = "\n\n".join(combined_text)
        
        return {
            "final_answer": final_response,
            "merged_sources": list(sources),
            "agents_used": [r.get("agent_id") for r in execution_results]
        }
