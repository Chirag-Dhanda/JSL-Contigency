from exceptions.base import AuthenticationException, AuthorizationException
from shared.error_codes import ErrorCode

class InvalidCredentialsException(AuthenticationException):
    def __init__(self):
        super().__init__(message="Invalid username or password.", error_code=ErrorCode.UNAUTHORIZED)

class AccountLockedException(AuthenticationException):
    def __init__(self):
        super().__init__(message="Account is locked due to multiple failed login attempts.", error_code=ErrorCode.FORBIDDEN)

class AccountInactiveException(AuthenticationException):
    def __init__(self):
        super().__init__(message="Account is inactive or suspended.", error_code=ErrorCode.FORBIDDEN)

class InvalidTokenException(AuthenticationException):
    def __init__(self):
        super().__init__(message="The provided token is invalid or expired.", error_code=ErrorCode.TOKEN_EXPIRED)
