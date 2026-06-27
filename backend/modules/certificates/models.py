from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from .enums import CertificateStatus

class EligibilityRule(BaseModel):
    min_score: Optional[float] = None
    mandatory_lessons: List[str] = []
    mandatory_assessments: List[str] = []
    required_competencies: Dict[str, float] = {} # e.g. {"SAFETY_AWARENESS": 80.0}
    requires_manager_approval: bool = False
    requires_department_approval: bool = False
    requires_hr_approval: bool = False

class CertificateTemplate(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    validity_period_days: Optional[int] = None # None means it doesn't expire
    eligibility: EligibilityRule

class Certificate(BaseModel):
    id: str
    certificate_number: str
    template_id: str
    user_id: str
    status: CertificateStatus = CertificateStatus.PENDING_APPROVAL
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    issued_by: Optional[str] = None
    approval_authority_id: Optional[str] = None
    verification_url: Optional[str] = None # Future
