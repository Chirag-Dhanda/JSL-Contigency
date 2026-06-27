from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# Note: Conceptual Domain Models. Not SQLAlchemy Entities yet.

class AccessLevel(str, Enum):
    """Configurable levels of access across the enterprise."""
    NO_ACCESS = "NO_ACCESS"
    OVERVIEW = "OVERVIEW"
    READ = "READ"
    COMMENT = "COMMENT"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    MANAGE = "MANAGE"
    ADMINISTER = "ADMINISTER"

class PermissionCategory(BaseModel):
    """Logical grouping of permissions (e.g., 'HR', 'Production', 'Logistics')."""
    id: str
    name: str
    description: Optional[str] = None

class PermissionGroup(BaseModel):
    """Sub-grouping within a category (e.g., 'Employee Records' under 'HR')."""
    id: str
    category_id: str
    name: str

class Permission(BaseModel):
    """A discrete enterprise permission (e.g., 'employee.update')."""
    id: str
    group_id: str
    code: str
    description: str
    access_level: AccessLevel
    
    # Future row-level security mapping
    resource_type: Optional[str] = None
    
class RolePermissionMapping(BaseModel):
    """Maps a Role to a Permission with optional overrides."""
    role_id: str
    permission_id: str
    is_revoked: bool = False # Allow explicitly blocking a permission from an inherited role
