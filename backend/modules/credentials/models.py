from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .enums import BadgeType, CompetencyLevel

class DigitalBadge(BaseModel):
    id: str
    user_id: str
    badge_type: BadgeType
    name: str
    description: str
    icon_url: str = ""
    earned_at: datetime
    linked_competency_level: Optional[CompetencyLevel] = None

class CredentialVerification(BaseModel):
    is_valid: bool
    message: str
    verification_type: str # "CERTIFICATE" or "BADGE"
    identifier: str
    issued_to: str
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status_enum: Optional[str] = None # String representation of the status
