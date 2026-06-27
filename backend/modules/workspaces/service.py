from typing import Dict, List, Optional
from datetime import datetime, timezone
from logging import getLogger

from .models import (
    WorkspaceContext, NavigationMenu, NavigationItem, 
    DepartmentLandingPage, Announcement, RoleType, DepartmentType,
    VisibilityLevel
)

logger = getLogger("WorkspaceEngine")

class WorkspaceEngine:
    def __init__(self):
        self._announcements: List[Announcement] = []
        self._department_pages: Dict[DepartmentType, DepartmentLandingPage] = {}
        self._mock_populate()

    def _mock_populate(self):
        """Pre-populate with configurable templates as per Implementation Plan 3.9."""
        self._department_pages[DepartmentType.PRODUCTION] = DepartmentLandingPage(
            department=DepartmentType.PRODUCTION,
            overview_text="Welcome to the Production Command Center.",
            sop_library_url="/library/sop/production",
            equipment_library_url="/library/equipment/production",
            featured_roadmaps=["roadmap_prod_safety", "roadmap_cnc_basics"]
        )

    def get_active_announcements(self, role: RoleType, department: DepartmentType) -> List[Announcement]:
        now = datetime.now(timezone.utc)
        active = []
        for ann in self._announcements:
            if ann.expires_at and ann.expires_at < now:
                continue
            if ann.target_roles and role not in ann.target_roles:
                continue
            if ann.target_departments and department not in ann.target_departments:
                continue
            active.append(ann)
        return active

    def generate_navigation(self, role: RoleType, department: DepartmentType) -> NavigationMenu:
        """Dynamically generates the navigation menu based on role and department."""
        # Base Menu for everyone
        main_menu = [
            NavigationItem(id="home", label="Dashboard", icon="home", route="/dashboard"),
            NavigationItem(id="learning", label="Learning Paths", icon="book", route="/learning")
        ]
        
        # Role specific
        if role in [RoleType.ADMINISTRATOR, RoleType.MANAGER, RoleType.DEPARTMENT_HEAD]:
            main_menu.append(NavigationItem(id="analytics", label="Analytics", icon="chart-bar", route="/analytics"))
            main_menu.append(NavigationItem(id="approvals", label="Approvals", icon="check-circle", route="/approvals"))

        # Department specific
        if department == DepartmentType.PRODUCTION:
            main_menu.append(NavigationItem(id="prod_sops", label="Production SOPs", icon="document", route="/sops/production"))

        return NavigationMenu(
            role=role,
            department=department,
            main_menu=main_menu,
            quick_access=[
                NavigationItem(id="quick_resume", label="Resume Last Lesson", icon="play", route="/learning/resume")
            ]
        )

    def get_workspace_context(self, user_id: str, role: RoleType, department: DepartmentType) -> WorkspaceContext:
        """Resolves the complete contextual workspace for the user."""
        logger.info(f"Resolving WorkspaceContext for User {user_id} ({role.value}, {department.value})")
        
        nav = self.generate_navigation(role, department)
        announcements = self.get_active_announcements(role, department)
        landing_page = self._department_pages.get(department)

        return WorkspaceContext(
            user_id=user_id,
            role=role,
            department=department,
            navigation=nav,
            landing_page=landing_page,
            active_announcements=announcements
        )
