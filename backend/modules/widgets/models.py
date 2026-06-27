from typing import List, Literal, Annotated, Union, Optional
from pydantic import BaseModel, Field

from .enums import WidgetType, WidgetSize

class BaseWidgetConfig(BaseModel):
    id: str
    title: str
    description: str
    allowed_sizes: List[WidgetSize]
    default_size: WidgetSize
    is_collapsible: bool = True
    is_resizable: bool = True
    required_permissions: List[str] = []

class WelcomeWidgetConfig(BaseWidgetConfig):
    type: Literal["WELCOME_CARD"] = "WELCOME_CARD"
    show_greeting: bool = True
    show_weather: bool = False

class ProgressWidgetConfig(BaseWidgetConfig):
    type: Literal["LEARNING_PROGRESS"] = "LEARNING_PROGRESS"
    display_style: str = "RING" # e.g., RING, BAR

class RoadmapWidgetConfig(BaseWidgetConfig):
    type: Literal["CURRENT_ROADMAP"] = "CURRENT_ROADMAP"
    max_steps_visible: int = 5

class TaskWidgetConfig(BaseWidgetConfig):
    type: Literal["TODAYS_TASKS"] = "TODAYS_TASKS"
    max_tasks: int = 10

class AssessmentWidgetConfig(BaseWidgetConfig):
    type: Literal["UPCOMING_ASSESSMENTS"] = "UPCOMING_ASSESSMENTS"
    days_lookahead: int = 7

class QuickActionConfig(BaseModel):
    action_id: str
    label: str
    icon_name: str
    target_url: str

class QuickActionsWidgetConfig(BaseWidgetConfig):
    type: Literal["QUICK_ACTIONS"] = "QUICK_ACTIONS"
    actions: List[QuickActionConfig]

class ActivityFeedWidgetConfig(BaseWidgetConfig):
    type: Literal["RECENT_ACTIVITY"] = "RECENT_ACTIVITY"
    max_items: int = 20

class AchievementWidgetConfig(BaseWidgetConfig):
    type: Literal["ACHIEVEMENTS"] = "ACHIEVEMENTS"
    show_recent_only: bool = True

class CertificateWidgetConfig(BaseWidgetConfig):
    type: Literal["CERTIFICATES"] = "CERTIFICATES"
    show_expired: bool = False

class NotificationWidgetConfig(BaseWidgetConfig):
    type: Literal["NOTIFICATIONS"] = "NOTIFICATIONS"
    max_notifications: int = 5

class DepartmentOverviewWidgetConfig(BaseWidgetConfig):
    type: Literal["DEPARTMENT_OVERVIEW"] = "DEPARTMENT_OVERVIEW"
    department_id: Optional[str] = None # Defaults to user's department

class LearningStatsWidgetConfig(BaseWidgetConfig):
    type: Literal["LEARNING_STATISTICS"] = "LEARNING_STATISTICS"
    metrics_to_show: List[str] = ["HOURS_SPENT", "COMPLETION_RATE"]

class ManufacturingJourneyWidgetConfig(BaseWidgetConfig):
    type: Literal["MANUFACTURING_JOURNEY"] = "MANUFACTURING_JOURNEY"
    show_map: bool = True

class AIAssistantWidgetConfig(BaseWidgetConfig):
    type: Literal["AI_ASSISTANT"] = "AI_ASSISTANT"
    placeholder_text: str = "Ask me anything..."

class SAPSummaryWidgetConfig(BaseWidgetConfig):
    type: Literal["SAP_SUMMARY"] = "SAP_SUMMARY"
    module_to_summarize: str = "HR"

WidgetConfig = Annotated[Union[
    WelcomeWidgetConfig,
    ProgressWidgetConfig,
    RoadmapWidgetConfig,
    TaskWidgetConfig,
    AssessmentWidgetConfig,
    QuickActionsWidgetConfig,
    ActivityFeedWidgetConfig,
    AchievementWidgetConfig,
    CertificateWidgetConfig,
    NotificationWidgetConfig,
    DepartmentOverviewWidgetConfig,
    LearningStatsWidgetConfig,
    ManufacturingJourneyWidgetConfig,
    AIAssistantWidgetConfig,
    SAPSummaryWidgetConfig
], Field(discriminator="type")]
