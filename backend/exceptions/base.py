from typing import Any, Dict, Optional, List
from shared.error_codes import ErrorCode

class BaseApplicationException(Exception):
    """Base exception for all enterprise application errors."""
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        error_code: str = ErrorCode.INTERNAL_ERROR,
        title: str = "Internal Server Error",
        developer_message: Optional[str] = None,
        validation_errors: Optional[List[Dict[str, Any]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.title = title
        self.developer_message = developer_message
        self.validation_errors = validation_errors
        super().__init__(self.message)

# ---------------------------------------------------------
# Client Errors (4xx)
# ---------------------------------------------------------
class ValidationException(BaseApplicationException):
    def __init__(self, message: str, validation_errors: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            message, 
            status_code=400, 
            error_code=ErrorCode.VALIDATION_ERROR,
            title="Validation Failed",
            validation_errors=validation_errors
        )

class AuthenticationException(BaseApplicationException):
    def __init__(self, message: str = "Authentication failed.", error_code: str = ErrorCode.UNAUTHORIZED):
        super().__init__(message, status_code=401, error_code=error_code, title="Unauthorized")

class AuthorizationException(BaseApplicationException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message, status_code=403, error_code=ErrorCode.FORBIDDEN, title="Forbidden")

class PermissionDeniedException(AuthorizationException):
    pass

class NotFoundException(BaseApplicationException):
    def __init__(self, message: str = "The requested resource could not be found."):
        super().__init__(message, status_code=404, error_code=ErrorCode.NOT_FOUND, title="Resource Not Found")

class ConflictException(BaseApplicationException):
    def __init__(self, message: str = "A conflict occurred with the current state of the resource."):
        super().__init__(message, status_code=409, error_code=ErrorCode.CONFLICT, title="Conflict")

class BusinessRuleException(BaseApplicationException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code=ErrorCode.BUSINESS_RULE_VIOLATION, title="Business Rule Violation")

# ---------------------------------------------------------
# Server Errors (5xx)
# ---------------------------------------------------------
class DatabaseException(BaseApplicationException):
    def __init__(self, message: str = "A database error occurred.", developer_message: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=ErrorCode.DATABASE_ERROR, title="Database Error", developer_message=developer_message)

class ConfigurationException(BaseApplicationException):
    def __init__(self, message: str = "A configuration error occurred."):
        super().__init__(message, status_code=500, error_code=ErrorCode.CONFIG_ERROR, title="Configuration Error")

class IntegrationException(BaseApplicationException):
    def __init__(self, message: str = "An external integration error occurred.", error_code: str = ErrorCode.INTEGRATION_ERROR):
        super().__init__(message, status_code=502, error_code=error_code, title="Integration Error")

class SAPException(IntegrationException):
    def __init__(self, message: str = "SAP integration failed."):
        super().__init__(message, error_code=ErrorCode.SAP_CONNECTION_ERROR)

class AIException(IntegrationException):
    def __init__(self, message: str = "AI service failed."):
        super().__init__(message, error_code=ErrorCode.AI_SERVICE_ERROR)

class StorageException(BaseApplicationException):
    def __init__(self, message: str = "A storage error occurred."):
        super().__init__(message, status_code=500, error_code=ErrorCode.INTERNAL_ERROR, title="Storage Error")

class ExternalServiceException(IntegrationException):
    pass

class SystemException(BaseApplicationException):
    def __init__(self, message: str = "A critical system error occurred.", developer_message: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=ErrorCode.INTERNAL_ERROR, title="System Error", developer_message=developer_message)
