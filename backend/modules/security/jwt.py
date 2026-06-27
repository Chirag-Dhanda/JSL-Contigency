import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple
from exceptions.base import SystemException, AuthenticationException
from shared.error_codes import ErrorCode
from logging import getLogger
from config.manager import get_config

logger = getLogger("JWTService")

class JWTService:
    """Service for encoding and decoding enterprise JWT tokens."""
    
    def __init__(self):
        # We load configuration at instantiation.
        config = get_config()
        self._secret = config.auth.jwt_secret
        self._algorithm = config.auth.jwt_algorithm
        self._access_expire_minutes = config.auth.access_token_expire_minutes
        
        # Optionally support a distinct config property for refresh tokens; otherwise default to 7 days
        self._refresh_expire_minutes = getattr(config.auth, "refresh_token_expire_minutes", 60 * 24 * 7)

    def generate_tokens(self, subject: str, extra_claims: Dict[str, Any] = None) -> Tuple[str, str, int]:
        """
        Generates both access and refresh tokens.
        Returns: (access_token, refresh_token, access_token_expires_in_seconds)
        """
        if not extra_claims:
            extra_claims = {}
            
        now = datetime.now(timezone.utc)
        
        # Access Token
        access_expires = now + timedelta(minutes=self._access_expire_minutes)
        access_payload = {
            "sub": subject,
            "exp": access_expires,
            "iat": now,
            "type": "access"
        }
        access_payload.update(extra_claims)
        access_token = jwt.encode(access_payload, self._secret, algorithm=self._algorithm)
        
        # Refresh Token
        refresh_expires = now + timedelta(minutes=self._refresh_expire_minutes)
        refresh_payload = {
            "sub": subject,
            "exp": refresh_expires,
            "iat": now,
            "type": "refresh"
        }
        refresh_token = jwt.encode(refresh_payload, self._secret, algorithm=self._algorithm)
        
        return access_token, refresh_token, self._access_expire_minutes * 60

    def decode_token(self, token: str, expected_type: str = "access") -> Dict[str, Any]:
        """
        Decodes and validates a token. 
        Throws AuthenticationException if expired, invalid, or wrong type.
        """
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            if payload.get("type") != expected_type:
                logger.warning(f"Token type mismatch. Expected {expected_type}, got {payload.get('type')}")
                raise AuthenticationException(message="Invalid token type.", error_code=ErrorCode.UNAUTHORIZED)
            return payload
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationException(message="Token has expired.", error_code=ErrorCode.TOKEN_EXPIRED)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT format: {e}")
            raise AuthenticationException(message="Invalid token structure.", error_code=ErrorCode.UNAUTHORIZED)
