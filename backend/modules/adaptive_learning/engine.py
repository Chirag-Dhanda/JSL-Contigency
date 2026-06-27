import logging
from typing import List, Dict, Any
from .roadmap import RoadmapAdapter

logger = logging.getLogger("AdaptiveLearningEngine")

class AdaptiveLearningEngine:
    """Core logic for adjusting the user's educational path."""
    
    def __init__(self):
        self.roadmap_adapter = RoadmapAdapter()

    def generate_next_steps(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Determines what the user should focus on next."""
        logger.debug("Generating next steps for adaptive learning")
        
        prioritized_path = self.roadmap_adapter.prioritize_learning_path(missing_skills)
        
        steps = []
        for i, skill in enumerate(prioritized_path[:3]): # Top 3
            steps.append({
                "module": skill,
                "reason": "Mandatory safety requirement" if "safety" in skill.lower() else "Role requirement",
                "priority": "High" if i == 0 else "Medium"
            })
            
        return steps
