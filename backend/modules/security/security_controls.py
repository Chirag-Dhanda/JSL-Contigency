from exceptions.base import AuthenticationException
from shared.error_codes import ErrorCode
from logging import getLogger
from typing import Dict

logger = getLogger("AccountLockoutService")

class AccountLockoutService:
    """Tracks failed authentication attempts and enforces temporary locks."""
    
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_MINUTES = 15
    
    def __init__(self):
        # Mock memory mapping user_id -> failed_count
        self._failed_attempts: Dict[str, int] = {}
        
    async def record_failed_attempt(self, user_id: str) -> None:
        current = self._failed_attempts.get(user_id, 0)
        self._failed_attempts[user_id] = current + 1
        logger.warning(f"Failed login attempt for user {user_id}. Count: {self._failed_attempts[user_id]}")
        
    async def reset_attempts(self, user_id: str) -> None:
        if user_id in self._failed_attempts:
            del self._failed_attempts[user_id]
            logger.debug(f"Reset failed attempts for user {user_id}")
            
    async def check_lockout(self, user_id: str) -> None:
        """Throws AuthenticationException if the account is currently locked by threshold."""
        attempts = self._failed_attempts.get(user_id, 0)
        if attempts >= self.MAX_FAILED_ATTEMPTS:
            logger.error(f"User {user_id} is locked out due to excessive failed attempts.")
            raise AuthenticationException(
                message="Account temporarily locked due to excessive failed attempts. Please try again later.",
                error_code=ErrorCode.UNAUTHORIZED
            )
