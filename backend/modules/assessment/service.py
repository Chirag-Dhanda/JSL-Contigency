from typing import Dict, Optional, List
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import Assessment, AssessmentAttempt, AssessmentResult
from .enums import AssessmentStatus

logger = getLogger("AssessmentService")

class AssessmentService:
    def __init__(self):
        self._assessments: Dict[str, Assessment] = {}
        self._attempts: Dict[str, AssessmentAttempt] = {}
        self._results: Dict[str, AssessmentResult] = {}

    def get_assessment(self, assessment_id: str) -> Optional[Assessment]:
        return self._assessments.get(assessment_id)

    def register_assessment(self, assessment: Assessment):
        self._assessments[assessment.id] = assessment
        logger.info(f"Registered Assessment: {assessment.title}")

    def start_attempt(self, user_id: str, assessment_id: str) -> AssessmentAttempt:
        """Initializes a new assessment attempt for a user."""
        if assessment_id not in self._assessments:
            raise ValueError("Assessment not found.")
            
        attempt_id = str(uuid.uuid4())
        attempt = AssessmentAttempt(
            id=attempt_id,
            user_id=user_id,
            assessment_id=assessment_id,
            status=AssessmentStatus.IN_PROGRESS,
            started_at=datetime.now(timezone.utc)
        )
        self._attempts[attempt_id] = attempt
        logger.info(f"Started attempt {attempt_id} for user {user_id}")
        return attempt

    def submit_answer(self, attempt_id: str, question_id: str, answer_payload: dict) -> AssessmentAttempt:
        """Saves an answer during an active attempt."""
        attempt = self._attempts.get(attempt_id)
        if not attempt or attempt.status != AssessmentStatus.IN_PROGRESS:
            raise ValueError("Invalid or inactive attempt.")
            
        attempt.answers[question_id] = answer_payload
        self._attempts[attempt_id] = attempt
        logger.debug(f"Saved answer for question {question_id} on attempt {attempt_id}")
        return attempt

    def finalize_attempt(self, attempt_id: str) -> AssessmentResult:
        """Submits the attempt and invokes the Scoring Engine."""
        attempt = self._attempts.get(attempt_id)
        if not attempt:
            raise ValueError("Attempt not found.")
            
        attempt.status = AssessmentStatus.SUBMITTED
        attempt.submitted_at = datetime.now(timezone.utc)
        
        # Invoke Scoring Engine
        result = self._score_attempt(attempt)
        
        attempt.status = AssessmentStatus.EVALUATED
        self._results[result.attempt_id] = result
        logger.info(f"Finalized attempt {attempt_id} with score {result.overall_score_percent}%")
        return result

    def _score_attempt(self, attempt: AssessmentAttempt) -> AssessmentResult:
        """Mock Scoring Engine logic."""
        assessment = self.get_assessment(attempt.assessment_id)
        
        # Mock calculation: assuming a random score based on mock logic
        # In a real engine, we would iterate through assessment.questions, validate against attempt.answers, apply points/negative_points
        
        overall_score = 85.0 # Mocked
        passed = overall_score >= assessment.passing_percentage
        
        result = AssessmentResult(
            attempt_id=attempt.id,
            user_id=attempt.user_id,
            assessment_id=assessment.id,
            overall_score_percent=overall_score,
            passed=passed,
            competency_scores={}, # Populated based on mapped_competencies of questions
            ai_feedback="Great job on manufacturing process questions. Review safety protocols."
        )
        return result
