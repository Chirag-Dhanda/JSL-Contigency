from pydantic import BaseModel
from typing import Optional, List

# Note: Conceptual Domain Models. Not SQLAlchemy Entities yet.

class Department(BaseModel):
    """A business unit within the organization."""
    id: str
    name: str
    code: str
    description: Optional[str] = None
    parent_department_id: Optional[str] = None
    head_employee_id: Optional[str] = None
    manager_employee_id: Optional[str] = None
    contact_email: Optional[str] = None
    status: str = "ACTIVE"
    
    # External Integration
    sap_cost_center: Optional[str] = None

class Role(BaseModel):
    """Dynamic organization roles (e.g. Administrator, Engineer, Shift Operator)."""
    id: str
    code: str
    title: str
    description: Optional[str] = None
    management_level: int = 0
    is_active: bool = True

class ReportingHierarchy(BaseModel):
    """Defines escalations and approval structures."""
    id: str
    employee_id: str
    approver_id: str
    escalation_id: Optional[str] = None
    level_depth: int = 0
    
    # Matrix Management (JSON arrays of IDs)
    management_chain: List[str] = []
    approval_chain: List[str] = []
