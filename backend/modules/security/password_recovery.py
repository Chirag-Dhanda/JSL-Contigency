from exceptions.base import SystemException
from logging import getLogger
from typing import Dict
from datetime import datetime, timezone, timedelta
import uuid

logger = getLogger("PasswordRecovery")

class PasswordRecoveryService:
    """Manages secure password reset tokens and temporary passwords."""
    
    def __init__(self):
        # Mock memory DB for reset tokens
        self._reset_tokens: Dict[str, dict] = {}
        
    async def generate_reset_token(self, user_id: str) -> str:
        token = str(uuid.uuid4())
        self._reset_tokens[token] = {
            "user_id": user_id,
            "expires_at": datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        logger.info(f"Generated password reset token for user {user_id}")
        return token
        
    async def validate_reset_token(self, token: str) -> str:
        """Returns the user_id if valid, or throws SystemException."""
        record = self._reset_tokens.get(token)
        if not record:
            raise SystemException("Invalid or missing reset token.")
        if record["expires_at"] < datetime.now(timezone.utc):
            del self._reset_tokens[token]
            raise SystemException("Reset token has expired.")
            
        del self._reset_tokens[token] # Single use
        return record["user_id"]
