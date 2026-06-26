class BaseAppException(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class ValidationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR")

class AuthenticationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")

class AuthorizationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")

class DatabaseException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")

class IntegrationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=502, error_code="INTEGRATION_ERROR")

class ConfigurationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="CONFIG_ERROR")
