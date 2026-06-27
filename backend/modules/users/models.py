from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from .enums import EmployeeStatus

# Note: Conceptual Domain Models. Not SQLAlchemy Entities yet.

class EmployeeMetadata(BaseModel):
    """Extensible metadata for dynamic properties without schema migrations."""
    properties: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    onboarding_completed: bool = False

class EmployeeProfile(BaseModel):
    """Personal and HR data for the employee."""
    first_name: str
    last_name: str
    contact_number: Optional[str] = None
    location: Optional[str] = None
    timezone: str = "UTC"
    hire_date: Optional[datetime] = None

class UserEntity(BaseModel):
    """The central User Domain entity."""
    id: str
    username: str
    email: str
    
    profile: EmployeeProfile
    status: EmployeeStatus = EmployeeStatus.PENDING_ONBOARDING
    metadata: EmployeeMetadata = Field(default_factory=EmployeeMetadata)
    
    # Relationships (Mapped via IDs to decouple domains)
    department_id: Optional[str] = None
    role_id: Optional[str] = None
    direct_manager_id: Optional[str] = None
    
    # Audit & Approval Chain
    created_by: Optional[str] = None
    approved_by: Optional[str] = None
    last_modified_by: Optional[str] = None
    
    # External Identifiers (Future Integration Placeholders)
    sap_employee_id: Optional[str] = None
    ldap_id: Optional[str] = None
    ad_id: Optional[str] = None
