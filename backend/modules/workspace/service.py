import logging
from typing import Dict, Optional
from .models import WorkspaceProfile, DashboardLayout, WidgetConfig, UserPreferences

logger = logging.getLogger("WorkspaceEngine")

class WorkspaceEngineService:
    """
    Manages Workspace Templates and generates personalized layouts based on roles.
    """
    def __init__(self):
        self._templates: Dict[str, DashboardLayout] = {}
        self._init_default_templates()
        logger.info("Workspace Engine Initialized.")

    def _init_default_templates(self):
        # Master Editor Template
        self._templates["MASTER_EDITOR"] = DashboardLayout(
            id="tpl-editor",
            name="Master Editor Workspace",
            widgets=[
                WidgetConfig(id="w1", type="system_stats", title="Platform Health", grid_area="span 1 / span 3"),
                WidgetConfig(id="w2", type="pending_reviews", title="Pending AI Intake Reviews", grid_area="span 2 / span 2"),
                WidgetConfig(id="w3", type="quick_actions", title="Quick Actions", grid_area="span 1 / span 1", settings={"actions": ["upload", "studio", "users"]})
            ]
        )
        
        # Engineer Template
        self._templates["ENGINEER"] = DashboardLayout(
            id="tpl-engineer",
            name="Engineer Workspace",
            widgets=[
                WidgetConfig(id="w1", type="equipment_status", title="Assigned Equipment", grid_area="span 2 / span 2"),
                WidgetConfig(id="w2", type="learning_progress", title="My Training", grid_area="span 1 / span 1"),
                WidgetConfig(id="w3", type="recent_assets", title="Recent CAD/Blueprints", grid_area="span 1 / span 3"),
                WidgetConfig(id="w4", type="quick_actions", title="Quick Actions", grid_area="span 1 / span 1", settings={"actions": ["sop", "ticket"]})
            ]
        )
        
        # Default Template
        self._templates["DEFAULT"] = DashboardLayout(
            id="tpl-default",
            name="General Workspace",
            widgets=[
                WidgetConfig(id="w1", type="announcements", title="Company Announcements", grid_area="span 1 / span 2"),
                WidgetConfig(id="w2", type="learning_progress", title="My Training", grid_area="span 1 / span 1"),
                WidgetConfig(id="w3", type="quick_actions", title="Quick Actions", grid_area="span 1 / span 1")
            ]
        )

    def get_workspace_for_user(self, user_id: str, role: str) -> WorkspaceProfile:
        logger.info(f"Generating personalized workspace for {user_id} (Role: {role})")
        
        # 1. Fetch Layout Template
        layout = self._templates.get(role, self._templates["DEFAULT"])
        
        # 2. Fetch User Preferences (mock)
        prefs = UserPreferences(theme="dark", accent_color="#3182ce")
        
        # 3. Assemble Profile
        profile = WorkspaceProfile(
            user_id=user_id,
            role=role,
            preferences=prefs,
            layout=layout
        )
        
        return profile
