from exceptions.base import SystemException
from typing import Optional, Dict
from datetime import datetime, timezone, timedelta
from .models import UserSession, LoginHistory
from logging import getLogger
import uuid

logger = getLogger("SessionManager")

class SessionManager:
    """Manages active user sessions and token revocation."""
    
    def __init__(self):
        # In-memory storage for functional testing
        self._active_sessions: Dict[str, UserSession] = {}
        self._audit_log: list[LoginHistory] = []
    
    async def create_session(self, user_id: str, jti: str, expires_in_minutes: int) -> UserSession:
        """Registers a new session in memory."""
        now = datetime.now(timezone.utc)
        session = UserSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token_jti=jti,
            created_at=now,
            expires_at=now + timedelta(minutes=expires_in_minutes),
            last_activity_at=now,
            is_active=True
        )
        self._active_sessions[jti] = session
        logger.debug(f"Created Session {session.id} for user {user_id}")
        return session
        
    async def is_session_active(self, jti: str) -> bool:
        """Checks if a specific JWT ID is still active."""
        session = self._active_sessions.get(jti)
        if not session:
            return False
        if not session.is_active:
            return False
        if session.expires_at < datetime.now(timezone.utc):
            session.is_active = False
            return False
        return True
        
    async def revoke_session(self, jti: str) -> None:
        """Revokes an active session."""
        session = self._active_sessions.get(jti)
        if session:
            session.is_active = False
            logger.info(f"Revoked session {session.id} manually.")
            
    async def revoke_all_sessions(self, user_id: str) -> None:
        """Revokes all sessions for a compromised or locked user."""
        count = 0
        for session in self._active_sessions.values():
            if session.user_id == user_id and session.is_active:
                session.is_active = False
                count += 1
        logger.warning(f"Revoked {count} sessions for user {user_id}.")

    async def log_authentication_attempt(self, username: str, status: str, user_id: Optional[str] = None) -> None:
        """Audit trail logging."""
        log = LoginHistory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            username_attempted=username,
            status=status,
            timestamp=datetime.now(timezone.utc)
        )
        self._audit_log.append(log)
        logger.info(f"Auth Audit: User {username} -> {status}")
