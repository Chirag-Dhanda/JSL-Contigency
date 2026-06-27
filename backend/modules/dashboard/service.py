from typing import Dict, List, Optional
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import DashboardLayout, DashboardPreference, WidgetInstance, ActivityItem
from backend.modules.widgets.service import WidgetRegistry
from backend.modules.workspaces.enums import RoleType, DepartmentType

logger = getLogger("DashboardEngine")

class DashboardEngine:
    def __init__(self, widget_registry: WidgetRegistry):
        self.widget_registry = widget_registry
        self._layouts: Dict[str, DashboardLayout] = {}
        self._preferences: Dict[str, DashboardPreference] = {}
        self._activity_feeds: Dict[str, List[ActivityItem]] = {}

    def get_preferences(self, user_id: str) -> DashboardPreference:
        if user_id not in self._preferences:
            self._preferences[user_id] = DashboardPreference(user_id=user_id)
        return self._preferences[user_id]

    def update_preferences(self, prefs: DashboardPreference):
        self._preferences[prefs.user_id] = prefs
        logger.info(f"Updated DashboardPreferences for User {prefs.user_id}")

    def get_layout(self, user_id: str, role: RoleType, department: DepartmentType) -> DashboardLayout:
        """Mock method generating a layout based on user role, department, and available widgets."""
        if user_id in self._layouts:
            return self._layouts[user_id]

        logger.info(f"Generating default DashboardLayout for User {user_id} (Role: {role.value}, Dept: {department.value})")
        
        # Mock getting available widgets for role
        available_widgets = self.widget_registry.get_available_widgets(user_permissions=[role.value])
        
        instances = []
        current_y = 0
        for i, config in enumerate(available_widgets):
            # Very naive mock grid generation
            instances.append(
                WidgetInstance(
                    instance_id=str(uuid.uuid4()),
                    x=0 if i % 2 == 0 else 6, # 12 column grid mock
                    y=current_y,
                    w=6,
                    h=4,
                    config=config
                )
            )
            if i % 2 != 0:
                current_y += 4

        layout = DashboardLayout(
            user_id=user_id,
            widgets=instances,
            last_updated=datetime.now(timezone.utc)
        )
        self._layouts[user_id] = layout
        return layout

    def log_activity(self, user_id: str, title: str, description: str, icon_name: str, action_url: Optional[str] = None):
        if user_id not in self._activity_feeds:
            self._activity_feeds[user_id] = []
            
        item = ActivityItem(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            description=description,
            icon_name=icon_name,
            timestamp=datetime.now(timezone.utc),
            action_url=action_url
        )
        
        # Keep feed trimmed
        self._activity_feeds[user_id].insert(0, item)
        if len(self._activity_feeds[user_id]) > 50:
            self._activity_feeds[user_id] = self._activity_feeds[user_id][:50]
            
        logger.debug(f"Logged activity for User {user_id}: {title}")

    def get_activity_feed(self, user_id: str) -> List[ActivityItem]:
        return self._activity_feeds.get(user_id, [])
