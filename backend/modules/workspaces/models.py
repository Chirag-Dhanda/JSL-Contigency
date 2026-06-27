from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from .enums import RoleType, DepartmentType, VisibilityLevel, AnnouncementType

class Announcement(BaseModel):
    id: str
    type: AnnouncementType
    title: str
    content: str
    target_roles: List[RoleType] = [] # Empty means all roles
    target_departments: List[DepartmentType] = [] # Empty means all departments
    published_at: datetime
    expires_at: Optional[datetime] = None

class NavigationItem(BaseModel):
    id: str
    label: str
    icon: str
    route: str
    visibility: VisibilityLevel = VisibilityLevel.VISIBLE
    children: List["NavigationItem"] = []

class NavigationMenu(BaseModel):
    role: RoleType
    department: DepartmentType
    pinned_modules: List[NavigationItem] = []
    main_menu: List[NavigationItem] = []
    recent_activity_links: List[NavigationItem] = []
    quick_access: List[NavigationItem] = []

class DepartmentLandingPage(BaseModel):
    department: DepartmentType
    overview_text: str
    sop_library_url: str
    equipment_library_url: str
    featured_roadmaps: List[str] # Roadmap IDs
    analytics_dashboard_id: Optional[str] = None

class WorkspaceContext(BaseModel):
    user_id: str
    role: RoleType
    department: DepartmentType
    navigation: NavigationMenu
    landing_page: Optional[DepartmentLandingPage] = None
    active_announcements: List[Announcement] = []
    
    # Theme configuration
    theme_preset: str = "industrial_light"
    accent_color: str = "#0052cc"

NavigationItem.model_rebuild()
