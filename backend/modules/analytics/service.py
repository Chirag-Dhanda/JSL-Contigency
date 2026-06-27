from typing import List, Optional
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import (
    EmployeeAnalytics, ManagerDashboardData, AdminDashboardData,
    Recommendation, RecommendationType, IndividualReport, DepartmentReport,
    RadarChart, RadarDataPoint, TrendGraph, TrendDataPoint, HeatMap, HeatMapCell
)
from backend.modules.competency.enums import CompetencyArea
from backend.modules.progress.service import ProgressEngine
# from backend.modules.competency.service import CompetencyService # (assuming it exists for the engine)

logger = getLogger("AnalyticsService")

class AnalyticsEngine:
    def __init__(self, progress_engine: ProgressEngine): # In a real scenario, we inject CompetencyService too
        self.progress_engine = progress_engine

    def get_employee_analytics(self, user_id: str) -> EmployeeAnalytics:
        logger.info(f"Generating EmployeeAnalytics for {user_id}")
        # Mock logic
        return EmployeeAnalytics(
            user_id=user_id,
            overall_progress_percent=75.5,
            learning_speed_metric=1.2,
            competency_radar=RadarChart(
                title="Competency Profile",
                data=[
                    RadarDataPoint(axis=CompetencyArea.SAFETY_AWARENESS.value, value=85.0),
                    RadarDataPoint(axis=CompetencyArea.MANUFACTURING_KNOWLEDGE.value, value=60.0)
                ]
            ),
            recent_activity=TrendGraph(
                title="Recent Activity (Hours)",
                series={"Hours Spent": [TrendDataPoint(timestamp=datetime.now(timezone.utc).isoformat(), value=2.5)]}
            ),
            pending_mandatory_count=2,
            certificates_earned=1
        )

    def get_manager_dashboard(self, manager_id: str) -> ManagerDashboardData:
        logger.info(f"Generating ManagerDashboardData for {manager_id}")
        return ManagerDashboardData(
            manager_id=manager_id,
            team_completion_percent=68.0,
            pending_training_count=12,
            expired_certifications_count=3,
            weak_competencies=[CompetencyArea.PROBLEM_SOLVING],
            top_performers_user_ids=["user_1", "user_2"],
            needs_assistance_user_ids=["user_3"],
            team_competency_radar=RadarChart(title="Team Competency", data=[]),
            progress_heatmap=HeatMap(title="Team Progress", cells=[])
        )

    def get_admin_dashboard(self) -> AdminDashboardData:
        logger.info("Generating AdminDashboardData")
        return AdminDashboardData(
            department_completion_heatmap=HeatMap(title="Department Completion", cells=[]),
            organization_learning_trend=TrendGraph(title="Org Trend", series={}),
            assessment_pass_rate_trend=TrendGraph(title="Pass Rates", series={}),
            competency_distribution={CompetencyArea.SAFETY_AWARENESS: 82.0},
            total_active_learners=1500,
            training_coverage_percent=92.5
        )

class RecommendationEngine:
    def generate_recommendations(self, user_id: str) -> List[Recommendation]:
        logger.info(f"Generating recommendations for {user_id}")
        # Mock logic based on weak competencies
        return [
            Recommendation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                target_entity_id="lesson_problem_solving_101",
                recommendation_type=RecommendationType.LESSON,
                reason="Based on your recent assessment, improving Problem Solving is recommended.",
                confidence_score=0.85
            )
        ]
