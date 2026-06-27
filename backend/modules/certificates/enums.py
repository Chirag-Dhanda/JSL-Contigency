from enum import Enum

class CertificateStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
