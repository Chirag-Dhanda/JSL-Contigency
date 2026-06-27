from enum import Enum

class ComplianceStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    EXPIRED = "EXPIRED"
    GRACE_PERIOD = "GRACE_PERIOD"
