import logging
from typing import Dict, Any

from .models import PersonalLearningProfile
from .analyzer import SkillGapAnalyzer
from .insights import InsightsGenerator
from .features import MentorFeatures

logger = logging.getLogger("LearningMentorEngine")

class LearningMentorEngine:
    """The central engine coordinating the learning mentor."""
    
    def __init__(self):
        self.analyzer = SkillGapAnalyzer()
        self.insights = InsightsGenerator()
        self.features = MentorFeatures()

    def get_mentor_dashboard_data(self, profile: PersonalLearningProfile, role_requirements: Dict) -> Dict[str, Any]:
        """Aggregates all mentor data for the frontend dashboard."""
        logger.info(f"Building Mentor Dashboard for {profile.user_id}")
        
        gaps = self.analyzer.analyze_gaps(profile, role_requirements)
        insights = self.insights.generate_insights(profile)
        daily_goal = self.features.generate_daily_goal(profile.user_id)
        
        return {
            "profile_summary": {
                "role": profile.role,
                "competencies": profile.competencies
            },
            "skill_gaps": gaps,
            "insights": insights,
            "daily_goal": daily_goal
        }
