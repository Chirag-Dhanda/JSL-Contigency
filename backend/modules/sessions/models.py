from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSession(BaseModel):
    """Tracks an active authenticated session."""
    id: str
    user_id: str
    token_jti: str  # JWT ID to allow specific token revocation
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    last_activity_at: datetime
    is_active: bool = True

class LoginHistory(BaseModel):
    """Audit trail for authentication attempts."""
    id: str
    user_id: Optional[str] = None
    username_attempted: str
    ip_address: Optional[str] = None
    status: str # SUCCESS, FAILED_PASSWORD, LOCKED, etc.
    timestamp: datetime
