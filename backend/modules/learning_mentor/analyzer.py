import logging
from typing import List, Dict
from .models import PersonalLearningProfile

logger = logging.getLogger("SkillGapAnalyzer")

class SkillGapAnalyzer:
    """Evaluates learning competency against role requirements."""
    
    def __init__(self):
        pass

    def analyze_gaps(self, profile: PersonalLearningProfile, role_requirements: Dict[str, List[str]]) -> List[str]:
        """Identifies missing lessons or competencies for the user's role."""
        logger.debug(f"Analyzing skill gaps for {profile.user_id} in role {profile.role}")
        
        required_lessons = role_requirements.get(profile.role, [])
        gaps = [lesson for lesson in required_lessons if lesson not in profile.completed_lessons]
        
        return gaps
