from enum import Enum

class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    ESCALATED = "ESCALATED"

class DurationType(str, Enum):
    PERMANENT = "PERMANENT"
    TEMPORARY = "TEMPORARY"
    EMERGENCY = "EMERGENCY"
