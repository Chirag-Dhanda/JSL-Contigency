from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import DepartmentType

class DepartmentAnnouncement(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    posted_at: datetime
    is_pinned: bool = False

class DepartmentLandingPage(BaseModel):
    department_type: DepartmentType
    mission: str
    responsibilities: List[str] = []
    reporting_structure_img_id: Optional[str] = None
    required_certifications: List[str] = []
    key_equipment_ids: List[str] = []
    manager_contact_id: Optional[str] = None

class DepartmentHub(BaseModel):
    id: str
    department_type: DepartmentType
    name: str
    landing_page: DepartmentLandingPage
    
    # Linked content arrays
    resource_ids: List[str] = []
    sop_ids: List[str] = []
    learning_library_ids: List[str] = []
    safety_library_ids: List[str] = []
    
    announcements: List[DepartmentAnnouncement] = []
    
    # Future AI Integration
    ai_assistant_prompt: Optional[str] = None
    # Future SAP Integration
    sap_dashboard_url: Optional[str] = None
