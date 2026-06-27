from enum import Enum

class ErrorCode(str, Enum):
    # System Errors
    INTERNAL_ERROR = "SYS-500"
    NOT_IMPLEMENTED = "SYS-501"
    SERVICE_UNAVAILABLE = "SYS-503"
    
    # Validation & Client Errors
    VALIDATION_ERROR = "VAL-400"
    NOT_FOUND = "REQ-404"
    CONFLICT = "REQ-409"
    UNPROCESSABLE = "REQ-422"
    
    # Authentication & Authorization
    UNAUTHORIZED = "AUTH-401"
    FORBIDDEN = "AUTH-403"
    TOKEN_EXPIRED = "AUTH-419"
    
    # Configuration
    CONFIG_ERROR = "CFG-500"
    
    # Database
    DATABASE_ERROR = "DB-500"
    RECORD_LOCKED = "DB-409"
    
    # Integrations
    INTEGRATION_ERROR = "INT-502"
    SAP_CONNECTION_ERROR = "SAP-502"
    AI_SERVICE_ERROR = "AI-502"
    
    # Business Logic
    BUSINESS_RULE_VIOLATION = "BIZ-400"
