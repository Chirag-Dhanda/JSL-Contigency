from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import ThemeMode
from backend.modules.widgets.models import WidgetConfig

class WidgetInstance(BaseModel):
    instance_id: str
    x: int # Grid X coordinate
    y: int # Grid Y coordinate
    w: int # Grid width
    h: int # Grid height
    is_pinned: bool = False
    config: WidgetConfig # The polymorphic config payload

class DashboardLayout(BaseModel):
    user_id: str
    widgets: List[WidgetInstance]
    last_updated: datetime

class DashboardPreference(BaseModel):
    user_id: str
    theme: ThemeMode = ThemeMode.SYSTEM
    favorite_widget_ids: List[str] = []
    hidden_widget_ids: List[str] = []

class ActivityItem(BaseModel):
    id: str
    user_id: str
    icon_name: str
    title: str
    description: str
    timestamp: datetime
    action_url: Optional[str] = None
