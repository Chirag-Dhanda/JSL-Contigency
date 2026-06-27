from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import ComplianceStatus

class ComplianceRule(BaseModel):
    id: str
    name: str
    description: str
    target_roles: List[str] = [] # Empty means all
    target_departments: List[str] = [] # Empty means all
    mandatory_module_ids: List[str] = []
    validity_period_days: Optional[int] = 365
    grace_period_days: int = 30

class UserComplianceRecord(BaseModel):
    id: str
    user_id: str
    rule_id: str
    status: ComplianceStatus
    completed_on: Optional[datetime] = None
    expires_on: Optional[datetime] = None
    grace_period_ends_on: Optional[datetime] = None

class SafetyDashboardStats(BaseModel):
    department_id: Optional[str] = None
    total_employees: int = 0
    compliant_employees: int = 0
    non_compliant_employees: int = 0
    grace_period_employees: int = 0
    compliance_percentage: float = 0.0
    pending_renewals_30_days: int = 0
