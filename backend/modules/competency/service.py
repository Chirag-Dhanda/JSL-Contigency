from typing import Dict
from datetime import datetime, timezone
from logging import getLogger

from .models import CompetencyProfile
from backend.modules.assessment.models import AssessmentResult

logger = getLogger("CompetencyService")

class CompetencyService:
    def __init__(self):
        self._profiles: Dict[str, CompetencyProfile] = {}

    def get_profile(self, user_id: str) -> CompetencyProfile:
        if user_id not in self._profiles:
            self._profiles[user_id] = CompetencyProfile(
                user_id=user_id,
                last_updated=datetime.now(timezone.utc)
            )
        return self._profiles[user_id]

    def evaluate_assessment_result(self, result: AssessmentResult) -> CompetencyProfile:
        """Evaluation Engine: Hooks into AssessmentResult to update CompetencyProfile."""
        profile = self.get_profile(result.user_id)
        
        # Mock logic to merge competency_scores into profile.area_scores
        # In a real engine, this would be a weighted rolling average or similar metric.
        for area, score in result.competency_scores.items():
            current_score = profile.area_scores.get(area, 0.0)
            # Simple average for mock
            profile.area_scores[area] = (current_score + score) / 2 if current_score > 0 else score
            
        if result.assessment_id not in profile.completed_assessments:
            profile.completed_assessments.append(result.assessment_id)
            
        # Mock overall readiness calculation
        if profile.area_scores:
            profile.overall_readiness_score = sum(profile.area_scores.values()) / len(profile.area_scores)
            
        profile.last_updated = datetime.now(timezone.utc)
        self._profiles[profile.user_id] = profile
        
        logger.info(f"Updated CompetencyProfile for user {profile.user_id} based on Assessment {result.assessment_id}")
        return profile
