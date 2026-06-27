from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class WidgetConfig(BaseModel):
    id: str
    type: str # e.g., 'learning_progress', 'quick_actions', 'announcements'
    title: str
    grid_area: str # e.g., 'span 2 / span 2'
    settings: Dict[str, Any] = Field(default_factory=dict)

class DashboardLayout(BaseModel):
    id: str
    name: str
    widgets: List[WidgetConfig] = Field(default_factory=list)

class UserPreferences(BaseModel):
    theme: str = "dark"
    accent_color: str = "blue"
    language: str = "en"
    pinned_modules: List[str] = Field(default_factory=list)

class WorkspaceProfile(BaseModel):
    user_id: str
    role: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    layout: DashboardLayout
    ai_recommendations: List[Dict[str, str]] = Field(default_factory=list)
