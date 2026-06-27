from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .enums import AccountStatus

# Note: These are conceptual domain models, not SQLAlchemy models yet.

class Role(BaseModel):
    id: str
    name: str

class Department(BaseModel):
    id: str
    name: str

class Permission(BaseModel):
    id: str
    code: str

class User(BaseModel):
    id: str
    username: str
    email: str
    status: AccountStatus
    roles: List[Role] = []
    departments: List[Department] = []
    permissions: List[Permission] = []
    failed_login_attempts: int = 0
    last_login: Optional[datetime] = None
