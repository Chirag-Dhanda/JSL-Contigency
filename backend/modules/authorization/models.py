from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResourceOwnership(BaseModel):
    """Standard tracking data attached to every secure entity in the platform."""
    resource_id: str
    created_by: str
    owned_by_dept_id: str
    last_modified_by: Optional[str] = None
    approved_by: Optional[str] = None
    
    # Future integration mapping
    sap_owner_id: Optional[str] = None

class CrossDepartmentAccess(BaseModel):
    """Explicitly grants an employee or role access to another department's resources."""
    id: str
    grantee_id: str # Can be user_id or role_id
    target_dept_id: str
    access_level: str # Overview, Read, Update, etc.
    granted_by: str
    expires_at: Optional[datetime] = None
    is_active: bool = True
