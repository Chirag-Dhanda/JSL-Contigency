from exceptions.base import SystemException, AuthenticationException
from shared.error_codes import ErrorCode
from .dto import LoginRequest, AuthResponse, PasswordResetRequest
from modules.users.enums import EmployeeStatus
from core.di import container

# Resolving cross-module services safely inside the class or lazily to avoid circular imports.
from modules.security.hashing import PasswordHasher
from modules.security.jwt import JWTService
from modules.security.security_controls import AccountLockoutService
from modules.sessions.service import SessionManager

from logging import getLogger
import uuid

logger = getLogger("AuthService")

class AuthService:
    """Core Authentication Logic and Token Dispensation."""
    
    def __init__(self):
        # We will set up a mock user DB for testing purposes so we can functionally test the pipeline.
        pwd_svc = container.resolve(PasswordHasher)
        self._mock_db = {
            "admin": {
                "id": "u-admin",
                "password_hash": pwd_svc.hash_password("admin123"),
                "status": EmployeeStatus.ACTIVE,
                "force_change": False
            },
            "newguy": {
                "id": "u-new",
                "password_hash": pwd_svc.hash_password("temp123"),
                "status": EmployeeStatus.PENDING_ONBOARDING,
                "force_change": True
            }
        }
    
    async def login(self, payload: LoginRequest) -> AuthResponse:
        logger.info(f"Attempting login for user: {payload.username}")
        
        lockout_svc = container.resolve(AccountLockoutService)
        session_svc = container.resolve(SessionManager)
        
        # 1. Pre-login checks
        await lockout_svc.check_lockout(payload.username)
        
        user_record = self._mock_db.get(payload.username)
        if not user_record:
            await lockout_svc.record_failed_attempt(payload.username)
            await session_svc.log_authentication_attempt(payload.username, "FAILED_NOT_FOUND")
            raise AuthenticationException(message="Invalid credentials.", error_code=ErrorCode.UNAUTHORIZED)

        # 2. Verify Password
        pwd_svc = container.resolve(PasswordHasher)
        if not pwd_svc.verify_password(payload.password, user_record["password_hash"]):
            await lockout_svc.record_failed_attempt(payload.username)
            await session_svc.log_authentication_attempt(payload.username, "FAILED_PASSWORD", user_id=user_record["id"])
            raise AuthenticationException(message="Invalid credentials.", error_code=ErrorCode.UNAUTHORIZED)
            
        # 3. Status Checks
        if user_record["status"] in [EmployeeStatus.LOCKED, EmployeeStatus.SUSPENDED]:
            await session_svc.log_authentication_attempt(payload.username, "BLOCKED_STATUS", user_id=user_record["id"])
            raise AuthenticationException(message="Account is suspended or locked.", error_code=ErrorCode.UNAUTHORIZED)
            
        if user_record["force_change"]:
            await session_svc.log_authentication_attempt(payload.username, "FORCE_CHANGE_REQUIRED", user_id=user_record["id"])
            raise AuthenticationException(message="First login requires password change.", error_code=ErrorCode.FORBIDDEN)
            
        # 4. Success Pipeline
        await lockout_svc.reset_attempts(payload.username)
        await session_svc.log_authentication_attempt(payload.username, "SUCCESS", user_id=user_record["id"])
        
        # 5. Generate Tokens
        jwt_svc = container.resolve(JWTService)
        jti = str(uuid.uuid4())
        access, refresh, exp_secs = jwt_svc.generate_tokens(user_record["id"], extra_claims={"jti": jti, "username": payload.username})
        
        # 6. Track Session
        await session_svc.create_session(user_id=user_record["id"], jti=jti, expires_in_minutes=exp_secs // 60)
        
        return AuthResponse(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_in=exp_secs
        )
        
    async def change_password(self, payload: PasswordResetRequest) -> None:
        """Process first-login password change."""
        user_record = self._mock_db.get(payload.username)
        if not user_record:
            raise AuthenticationException("Invalid user.")
            
        pwd_svc = container.resolve(PasswordHasher)
        if not pwd_svc.verify_password(payload.current_password, user_record["password_hash"]):
            raise AuthenticationException("Invalid credentials.")
            
        # Apply change
        user_record["password_hash"] = pwd_svc.hash_password(payload.new_password)
        user_record["force_change"] = False
        user_record["status"] = EmployeeStatus.ACTIVE
        logger.info(f"Password changed successfully for {payload.username}")
        
    async def logout(self, jti: str) -> None:
        session_svc = container.resolve(SessionManager)
        await session_svc.revoke_session(jti)
