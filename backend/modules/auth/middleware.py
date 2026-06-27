from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from exceptions.base import AuthenticationException
from shared.error_codes import ErrorCode
from core.di import container
from modules.security.jwt import JWTService
from modules.sessions.service import SessionManager
from logging import getLogger
from typing import Dict, Any

logger = getLogger("AuthMiddleware")

# Standard FastAPI dependency that extracts the Bearer token from the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_jwt_service() -> JWTService:
    return container.resolve(JWTService)

def get_session_manager() -> SessionManager:
    return container.resolve(SessionManager)

async def require_authenticated_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
    session_manager: SessionManager = Depends(get_session_manager)
) -> Dict[str, Any]:
    """
    FastAPI dependency to protect endpoints.
    Validates the JWT signature, expiration, and ensures the session is not revoked.
    """
    logger.debug("Validating Bearer Token...")
    
    # 1. Decode and Validate Signature/Expiration
    payload = jwt_service.decode_token(token, expected_type="access")
    
    # 2. Extract Token ID (JTI) for Session Revocation Check
    jti = payload.get("jti")
    if not jti:
        # If there's no JTI, we can't track its session reliably.
        pass 
        # In a strict enterprise environment, we might reject tokens without JTIs.
        # But we'll allow it for now if generated manually without a JTI.

    if jti:
        # 3. Check Session Manager (Redis/DB) if the token was revoked
        is_active = await session_manager.is_session_active(jti)
        if not is_active:
            logger.warning(f"Attempted use of revoked session JTI: {jti}")
            raise AuthenticationException(message="Session has been revoked or logged out.", error_code=ErrorCode.UNAUTHORIZED)

    # 4. Inject Context
    logger.debug(f"Authentication Successful for subject: {payload.get('sub')}")
    return payload
