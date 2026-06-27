import logging
from typing import List, Dict, Any

logger = logging.getLogger("RecommendationEngine")

class RecommendationEngine:
    """Formats the adaptive learning steps into actionable recommendations for the UI."""
    
    def __init__(self):
        pass

    def get_recommendations(self, adaptive_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Wraps the adaptive logic with UX friendly metadata."""
        logger.debug("Formatting final recommendations")
        
        recommendations = []
        for step in adaptive_steps:
            recommendations.append({
                "title": f"Complete: {step['module']}",
                "description": step['reason'],
                "action_type": "Start Module",
                "priority_badge": step['priority']
            })
            
        return recommendations
