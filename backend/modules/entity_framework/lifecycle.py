from enum import Enum

class EntityLifecycle(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    DEPRECATED = "DEPRECATED"
    DELETED = "DELETED"
