from enum import Enum

class NotificationType(str, Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    LEARNING = "LEARNING"
    APPROVAL = "APPROVAL"
    SECURITY = "SECURITY"

class DeliveryChannel(str, Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    SMS = "SMS"
    TEAMS = "TEAMS"

class Priority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class NotificationStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    DELIVERED = "DELIVERED"
    READ = "READ"
    FAILED = "FAILED"
