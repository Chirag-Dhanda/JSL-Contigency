from typing import Dict, List, Optional
from logging import getLogger
import uuid

from .models import WidgetConfig, WidgetType
from .enums import WidgetSize

logger = getLogger("WidgetRegistry")

class WidgetRegistry:
    def __init__(self):
        self._widgets: Dict[str, WidgetConfig] = {}

    def register_widget(self, config: WidgetConfig):
        self._widgets[config.id] = config
        logger.info(f"Registered Widget: {config.title} ({config.type.value})")

    def get_widget(self, widget_id: str) -> Optional[WidgetConfig]:
        return self._widgets.get(widget_id)

    def get_available_widgets(self, user_permissions: List[str] = []) -> List[WidgetConfig]:
        """Returns widgets the user has permission to view."""
        available = []
        for widget in self._widgets.values():
            # Mock permission check: If widget requires permissions, ensure user has all of them
            has_perms = all(perm in user_permissions for perm in widget.required_permissions)
            if has_perms:
                available.append(widget)
        return available
