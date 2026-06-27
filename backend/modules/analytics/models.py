from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from backend.modules.competency.enums import CompetencyArea

class RecommendationType(str, Enum):
    LESSON = "LESSON"
    ASSESSMENT = "ASSESSMENT"
    ROADMAP = "ROADMAP"
    CERTIFICATE = "CERTIFICATE"

# ---------------------------------------------------------
# Visualization Models
# ---------------------------------------------------------

class TrendDataPoint(BaseModel):
    timestamp: str # ISO format
    value: float

class TrendGraph(BaseModel):
    title: str
    series: Dict[str, List[TrendDataPoint]] # e.g., "Completion %": [...]

class RadarDataPoint(BaseModel):
    axis: str # e.g., Competency Area
    value: float
    full_mark: float = 100.0

class RadarChart(BaseModel):
    title: str
    data: List[RadarDataPoint]

class HeatMapCell(BaseModel):
    x_label: str
    y_label: str
    intensity: float # 0.0 to 1.0

class HeatMap(BaseModel):
    title: str
    cells: List[HeatMapCell]

# ---------------------------------------------------------
# Dashboard Models
# ---------------------------------------------------------

class EmployeeAnalytics(BaseModel):
    user_id: str
    overall_progress_percent: float
    learning_speed_metric: float # Custom internal metric
    competency_radar: RadarChart
    recent_activity: TrendGraph
    pending_mandatory_count: int
    certificates_earned: int

class ManagerDashboardData(BaseModel):
    manager_id: str
    team_completion_percent: float
    pending_training_count: int
    expired_certifications_count: int
    weak_competencies: List[CompetencyArea]
    top_performers_user_ids: List[str]
    needs_assistance_user_ids: List[str]
    team_competency_radar: RadarChart
    progress_heatmap: HeatMap

class AdminDashboardData(BaseModel):
    department_completion_heatmap: HeatMap
    organization_learning_trend: TrendGraph
    assessment_pass_rate_trend: TrendGraph
    competency_distribution: Dict[CompetencyArea, float]
    total_active_learners: int
    training_coverage_percent: float

# ---------------------------------------------------------
# Recommendation & Reporting
# ---------------------------------------------------------

class Recommendation(BaseModel):
    id: str
    user_id: str
    target_entity_id: str
    recommendation_type: RecommendationType
    reason: str
    confidence_score: float # Mock AI confidence

class IndividualReport(BaseModel):
    user_id: str
    generated_at: datetime
    analytics: EmployeeAnalytics
    recommendations: List[Recommendation]

class DepartmentReport(BaseModel):
    department_name: str
    generated_at: datetime
    team_completion_percent: float
    weakest_competency: CompetencyArea
    strongest_competency: CompetencyArea
